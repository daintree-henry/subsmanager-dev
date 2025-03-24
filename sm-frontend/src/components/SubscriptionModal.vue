<template>
  <div>
    <!-- Subscription Modal -->
    <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg p-6 w-full max-w-md">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-xl font-bold">Subscribe to {{ planName }}</h3>
          <button @click="close" class="text-gray-500 hover:text-gray-700">
            <span class="text-2xl">&times;</span>
          </button>
        </div>

        <form @submit.prevent="handleSubmit" class="space-y-4">
          <!-- 구독 정보 -->
          <div>
            <h4 class="font-semibold mb-2">Subscription Details</h4>
            <div class="space-y-3">
              <div>
                <label class="block text-sm font-medium text-gray-700">Auto Renewal</label>
                <div class="mt-1">
                  <input
                    type="checkbox"
                    v-model="formData.auto_renewal"
                    class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                  >
                  <span class="ml-2 text-sm text-gray-600">Enable auto renewal</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 결제 정보 -->
          <div>
            <h4 class="font-semibold mb-2">Payment Information</h4>
            <div class="space-y-3">
              <div>
                <label class="block text-sm font-medium text-gray-700">Payment Method</label>
                <select
                  v-model="formData.payment_method"
                  class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-green-500 focus:ring-green-500"
                  required
                >
                  <option value="credit_card">Credit Card</option>
                  <option value="debit_card">Debit Card</option>
                  <option value="bank_transfer">Bank Transfer</option>
                </select>
              </div>
            </div>
          </div>

          <div class="pt-4">
            <button
              type="submit"
              class="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              :disabled="loading"
            >
              <template v-if="loading">
                <span class="inline-block animate-pulse">Processing...</span>
              </template>
              <template v-else>
                Confirm Subscription
              </template>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Success Notification -->
    <div v-if="showSuccessNotification" class="fixed top-5 right-5 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded shadow-md z-50">
      <div class="flex items-center">
        <div class="py-1">
          <svg class="h-6 w-6 text-green-500 mr-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
        </div>
        <div>
          <p class="font-bold">Success!</p>
          <p class="text-sm">Subscription has been successfully added.</p>
        </div>
        <button @click="closeNotification" class="ml-auto">
          <span class="text-green-500 hover:text-green-700">&times;</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';

export default {
  name: 'SubscriptionModal',
  props: {
    show: {
      type: Boolean,
      required: true
    },
    planId: {
      type: Number,
    },
    planName: {
      type: String,
    },
    monthlyFee: {
      type: Number,
    }
  },
  emits: ['close', 'submit'],
  setup(props, { emit }) {
    const loading = ref(false);
    const showSuccessNotification = ref(false);

    const close = () => {
      emit('close');
      formData.value = {
        start_date: today.value,
        auto_renewal: true,
        payment_method: 'credit_card',
      };
    };

    const closeNotification = () => {
      showSuccessNotification.value = false;
    };

    const formattedDate = (date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    };

    const today = computed(() => {
      return formattedDate(new Date());
    });

    const formData = ref({
      start_date: formattedDate(new Date()),
      auto_renewal: true,
      payment_method: 'credit_card',
    });

    const handleSubmit = async () => {
      const userConfirmed = window.confirm("Are you sure you want to add subscription and payment information?");

      if (!userConfirmed) {
        return;
      }

      loading.value = true;
      try {
        const today = new Date();
        const startDate = formattedDate(today);

        const nextBillingDate = new Date(today);
        nextBillingDate.setMonth(nextBillingDate.getMonth() + 1);
        const formattedNextBillingDate = formattedDate(nextBillingDate);

        const subscriptionData = {
          subscription_plan_id: props.planId,
          start_date: startDate,
          next_billing_date: formattedNextBillingDate,
          auto_renewal: formData.value.auto_renewal,
          payment_method: formData.value.payment_method,
          payment: {
            amount_paid: props.monthlyFee,
            payment_method: formData.value.payment_method,
          }
        };

        emit('submit', subscriptionData);
        close();

        // Show success notification
        showSuccessNotification.value = true;

        // Auto-hide notification after 5 seconds
        setTimeout(() => {
          showSuccessNotification.value = false;
        }, 5000);

      } finally {
        loading.value = false;
      }
    };

    return {
      loading,
      formData,
      today,
      close,
      handleSubmit,
      showSuccessNotification,
      closeNotification
    };
  }
};
</script>