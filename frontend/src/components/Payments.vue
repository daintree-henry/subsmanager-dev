<template>
  <div class="h-full w-full flex flex-col mt-20">
    <div class="flex-1 overflow-y-auto">
      <div class="container mx-auto px-4 py-8">
        <div class="mb-8 p-6 bg-white rounded-lg shadow-md">
          <!-- 에러 메시지 표시 -->
          <div v-if="error" class="mb-4 p-4 bg-red-100 text-red-700 rounded">
            {{ error }}
          </div>

          <div class="mt-8">
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl font-bold">Payment History</h3>

              <!-- 상태 필터 -->
              <select
                v-model="selectedStatus"
                @change="fetchPayments"
                class="px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">All Status</option>
                <option value="successful">Successful</option>
                <option value="pending">Pending</option>
                <option value="failed">Failed</option>
                <option value="refunded">Refunded</option>
              </select>
            </div>

            <!-- 로딩 상태 표시 -->
            <div v-if="loading" class="text-center py-4">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto"></div>
              <p class="mt-2 text-gray-600">Loading payments...</p>
            </div>

            <!-- 결제 내역 테이블 -->
            <div v-else class="overflow-x-auto">
              <table class="min-w-full bg-white border rounded-lg">
                <thead class="bg-gray-50">
                  <tr>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Date
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Provider/Plan
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Amount
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Status
                    </th>
                    <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Payment Method
                    </th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-gray-200">
                  <tr v-for="payment in payments" :key="payment.id">
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ formatDate(payment.payment_date) }}
                    </td>
                    <td class="px-6 py-4">
                      <div class="flex flex-col">
                        <span class="text-sm font-medium text-gray-900">
                          {{ payment.provider_name }}
                        </span>
                        <span class="text-sm text-gray-500">
                          {{ payment.plan_name }}
                        </span>
                      </div>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      $ {{ formatPrice(payment.amount_paid) }}
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap">
                      <span :class="getStatusClass(payment.payment_status)"
                            class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                        {{ payment.payment_status }}
                      </span>
                    </td>
                    <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {{ payment.payment_method }}
                    </td>
                  </tr>
                </tbody>
              </table>

              <!-- 데이터가 없을 경우 -->
              <div v-if="payments.length === 0" class="text-center py-8 text-gray-500">
                No payment history found.
              </div>
            </div>

            <!-- 페이지네이션 -->
            <div v-if="totalPages > 1" class="flex justify-center gap-2 mt-6">
              <button
                @click="changePage(currentPage - 1)"
                :disabled="currentPage === 1"
                class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Previous
              </button>
              <button
                v-for="page in totalPages"
                :key="page"
                @click="changePage(page)"
                :class="{'bg-green-500 text-white': currentPage === page}"
                class="px-4 py-2 border rounded-lg hover:bg-gray-50"
              >
                {{ page }}
              </button>
              <button
                @click="changePage(currentPage + 1)"
                :disabled="currentPage === totalPages"
                class="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50"
              >
                Next
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted} from 'vue';
import { subAPI } from '@/api/axios';

export default {
  name: 'PaymentHistory',
  setup() {
    const loading = ref(false);
    const error = ref(null);
    const payments = ref([]);
    const currentPage = ref(1);
    const totalPages = ref(0);
    const selectedStatus = ref('');
    const perPage = 10;

    const fetchPayments = async () => {
      loading.value = true;
      error.value = null;
      try {
        const params = {
          page: currentPage.value,
          per_page: perPage
        };

        if (selectedStatus.value) {
          params.status = selectedStatus.value;
        }

        const response = await subAPI.get(
            `/sub/payments`,
            {
              params
            }
        );

        payments.value = response.data.items;
        totalPages.value = response.data.pages;
        currentPage.value = response.data.current_page;
      } catch (err) {
        error.value = '결제 내역을 불러오는데 실패했습니다.';
        console.error('Error fetching payments:', err);
      } finally {
        loading.value = false;
      }
    };

    const changePage = (page) => {
      if (page >= 1 && page <= totalPages.value) {
        currentPage.value = page;
        fetchPayments();
      }
    };

    const formatDate = (dateString) => {
      return new Date(dateString).toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      });
    };

    const formatPrice = (price) => {
      return price.toLocaleString('en-US', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      });
    };

    const getStatusClass = (status) => {
      const classes = {
        successful: 'bg-green-100 text-green-800',
        pending: 'bg-yellow-100 text-yellow-800',
        failed: 'bg-red-100 text-red-800',
        refunded: 'bg-gray-100 text-gray-800'
      };
      return classes[status] || 'bg-gray-100 text-gray-800';
    };

    onMounted(() => {
      fetchPayments();
    });

    return {
      loading,
      error,
      payments,
      currentPage,
      totalPages,
      selectedStatus,
      fetchPayments,
      changePage,
      formatDate,
      formatPrice,
      getStatusClass
    };
  }
};
</script>