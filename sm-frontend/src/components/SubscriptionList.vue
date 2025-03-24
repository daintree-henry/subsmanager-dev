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
            <h3 class="text-xl font-bold mb-4">Available Plans</h3>
            <!-- 로딩 상태 표시 -->
            <div v-if="loading" class="text-center py-4">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mx-auto"></div>
              <p class="mt-2 text-gray-600">Loading plans...</p>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 h-[32rem] overflow-y-auto mb-4">
              <div v-for="plan in subscriptionPlans" :key="plan.id"
                   class="p-4 border rounded-lg shadow hover:shadow-md transition-shadow">
                <div class="h-full flex flex-col">
                  <div class="flex items-center gap-3 mb-4">
                    <img :src="`/images/providers/${plan.logo_file_name}`"
                         :alt="plan.plan_name"
                         class="h-10 w-10 object-contain rounded-md shadow-md">
                    <div class="flex flex-col">
                      <h4 class="font-semibold text-gray-800 text-lg">{{ plan.provider_name }}</h4>
                      <h4 class="text-gray-600 text-sm">{{ plan.plan_name }}</h4>
                    </div>
                  </div>
                  <p class="text-lg font-semibold text-green-600 mb-4">$ {{ formatPrice(plan.monthly_fee) }}/month</p>

                  <div class="mb-4 flex-grow overflow-y-auto">
                    <h5 class="font-medium mb-2">Features:</h5>
                    <ul class="text-sm space-y-1">
                      <li v-if="plan.features.resolution">
                        • Resolution: {{ plan.features.resolution }}
                      </li>
                      <li v-if="plan.features.concurrent_streams">
                        • {{ plan.features.concurrent_streams }} concurrent streams
                      </li>
                      <li v-if="plan.features.downloads">
                        • Downloads available
                      </li>
                      <li v-if="plan.features.ad_free === true">
                        • Ad-free
                      </li>
                      <li v-if="plan.features.shared_with_family === true">
                        • Family Shared
                      </li>
                      <li v-if="plan.features.dolby_atmos === true">
                        • Dolby Atmos
                      </li>
                      <li v-if="plan.features.dolby_vision === true">
                        • Dolby Vision
                      </li>
                      <li v-if="plan.features.ads === false">
                        • Ad-free
                      </li>
                      <li v-if="plan.features.siri_only === true">
                        • Siri Only
                      </li>
                      <li v-if="plan.features.spatial_audio === true">
                        • Spatial audio
                      </li>
                      <li v-if="plan.features.family_members">
                        • Up to {{ plan.features.family_members }} family members
                      </li>
                      <li v-if="plan.features.high_quality_audio === true">
                        • High quality audio
                      </li>
                      <li v-if="plan.features.lossless_audio === true">
                        • Lossless Audio
                      </li>
                      <li v-if="plan.features.lyrics_view === true">
                        • Lyrics View
                      </li>
                      <li v-if="plan.features.offline_mode === true">
                        • Offline Mode
                      </li>
                      <li v-if="plan.features.playlist_sharing === true">
                        • Playlist Sharing
                      </li>
                      <li v-if="plan.features.background_play === true">
                        • Background Play
                      </li>
                      <li v-if="plan.features.offline_mixtape === true">
                        • Offline Mixtape
                      </li>
                      <li v-if="plan.features.student_verification === true">
                        • Student Verification
                      </li>
                      <li v-if="plan.features.duo_mix === true">
                        • Duo_mix
                      </li>
                      <li v-if="plan.features.family_mix === true">
                        • Family Mix
                      </li>
                      <li v-if="plan.features.parental_controls === true">
                        • Parental Controls
                      </li>
                    </ul>
                  </div>

                  <button
                    @click="openSubscriptionModal(plan)"
                    :disabled="loading"
                    class="w-full bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors mt-auto disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <template v-if="loading">
                      <span class="inline-block animate-pulse">Processing...</span>
                    </template>
                    <template v-else>
                      Add Subscription
                    </template>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- 구독 모달 -->
          <SubscriptionModal
            :show="showModal"
            :planId="selectedPlan?.id"
            :planName="selectedPlan?.plan_name"
            :monthlyFee="selectedPlan?.monthly_fee"
            @close="closeSubscriptionModal"
            @submit="handleSubscriptionSubmit"
          />

          <!-- 성공 메시지 토스트 -->
          <div v-if="showSuccess"
               class="fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg transition-opacity duration-300"
               :class="{ 'opacity-0': !showSuccess }">
            Subscription added successfully!
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { subAPI } from '@/api/axios';
import SubscriptionModal from './SubscriptionModal.vue';

export default {
  name: 'SubscriptionList',
  components: {
    SubscriptionModal
  },
  setup() {
    const loading = ref(false);
    const error = ref(null);
    const subscriptionPlans = ref([]);
    const showModal = ref(false);
    const selectedPlan = ref(null);
    const showSuccess = ref(false);

    const fetchSubscriptionPlans = async () => {
      loading.value = true;
      error.value = null;
      try {
        const response = await subAPI.get(
          `/sub/plans`,
        );
        subscriptionPlans.value = response.data;
      } catch (err) {
        error.value = '구독 플랜을 불러오는데 실패했습니다.';
        console.error('Error fetching subscription plans:', err);
      } finally {
        loading.value = false;
      }
    };

    const openSubscriptionModal = (plan) => {
      selectedPlan.value = plan;
      showModal.value = true;
    };

    const closeSubscriptionModal = () => {
      showModal.value = false;
      selectedPlan.value = null;
    };

    const handleSubscriptionSubmit = async (subscriptionData) => {
      loading.value = true;
      error.value = null;
      try {
        // 구독 생성
        const subscriptionResponse = await subAPI.post(
          `/sub`,
          {
            subscription_plan_id: subscriptionData.subscription_plan_id,
            start_date: subscriptionData.start_date,
            next_billing_date: subscriptionData.next_billing_date,
            auto_renewal: subscriptionData.auto_renewal,
            payment_method: subscriptionData.payment_method,
            status: 'active'
          },
        );

        // 결제 생성
        if (subscriptionResponse.data.id) {
          await subAPI.post(
            `/sub/payments`,
            {
              user_subscription_id: subscriptionResponse.data.id,
              amount_paid: subscriptionData.payment.amount_paid,
              payment_method: subscriptionData.payment.payment_method,
              payment_status: 'successful'
            },
          );
        }

        // 성공 메시지 표시
        showSuccess.value = true;
        setTimeout(() => {
          showSuccess.value = false;
        }, 3000);

      } catch (err) {
        if (err.response?.status === 409) {
          error.value = err.response.data.message || '이미 활성화된 구독이 있습니다.';
        } else {
          error.value = '구독 추가에 실패했습니다.';
        }
        console.error('Error adding subscription:', err);
      } finally {
        loading.value = false;
      }
    };

    const formatPrice = (price) => {
      return price.toLocaleString();
    };

    onMounted(() => {
      fetchSubscriptionPlans();
    });

    return {
      loading,
      error,
      subscriptionPlans,
      showModal,
      selectedPlan,
      showSuccess,
      openSubscriptionModal,
      closeSubscriptionModal,
      handleSubscriptionSubmit,
      formatPrice
    };
  }
};
</script>