<template>
  <div class="h-full w-full flex flex-col mt-20">
    <div class="flex-1 overflow-y-auto">
      <div class="container mx-auto px-4 py-8">
        <div v-if="recommendations.length" class="p-6 bg-white rounded-lg shadow-md mt-8">
          <h2 class="text-2xl font-bold mb-4">Recommended Plans</h2>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div v-for="rec in recommendations" :key="rec.plan_id"
                 class="p-4 border rounded-lg hover:shadow-md transition-shadow">
              <div class="flex items-center justify-between mb-3">
                <div>
                  <p class="text-lg font-semibold">{{ rec.provider_name }}</p>
                  <h3 class="text-gray-600">Plan: {{ rec.plan_name }}</h3>
                </div>
                <img
                  :src="`/images/providers/${rec.logo_file_name}`"
                  :alt="rec.plan_name"
                  class="h-10 w-10 object-contain rounded-md shadow-sm"
                >
              </div>
              <p class="text-gray-600 mb-3">Monthly Fee: ${{ rec.monthly_fee }}</p>
              <div class="mb-4 flex-grow overflow-y-auto">
                <h5 class="font-medium mb-2">Features:</h5>
                  <ul class="text-sm space-y-1">
                    <li v-if="rec.features.resolution">
                      • Resolution: {{ rec.features.resolution }}
                    </li>
                    <li v-if="rec.features.concurrent_streams">
                      • {{ rec.features.concurrent_streams }} concurrent streams
                    </li>
                    <li v-if="rec.features.downloads">
                      • Downloads available
                    </li>
                    <li v-if="rec.features.ad_free === true">
                      • Ad-free
                    </li>
                    <li v-if="rec.features.shared_with_family === true">
                      • Family Shared
                    </li>
                    <li v-if="rec.features.dolby_atmos === true">
                      • Dolby Atmos
                    </li>
                    <li v-if="rec.features.dolby_vision === true">
                      • Dolby Vision
                    </li>
                    <li v-if="rec.features.ads === false">
                      • Ad-free
                    </li>
                    <li v-if="rec.features.siri_only === true">
                      • Siri Only
                    </li>
                    <li v-if="rec.features.spatial_audio === true">
                      • Spatial audio
                    </li>
                    <li v-if="rec.features.family_members">
                      • Up to {{ rec.features.family_members }} family members
                    </li>
                    <li v-if="rec.features.high_quality_audio === true">
                      • High quality audio
                    </li>
                    <li v-if="rec.features.lossless_audio === true">
                      • Lossless Audio
                    </li>
                    <li v-if="rec.features.lyrics_view === true">
                      • Lyrics View
                    </li>
                    <li v-if="rec.features.offline_mode === true">
                      • Offline Mode
                    </li>
                    <li v-if="rec.features.playlist_sharing === true">
                      • Playlist Sharing
                    </li>
                    <li v-if="rec.features.background_play === true">
                      • Background Play
                    </li>
                    <li v-if="rec.features.offline_mixtape === true">
                      • Offline Mixtape
                    </li>
                    <li v-if="rec.features.student_verification === true">
                      • Student Verification
                    </li>
                    <li v-if="rec.features.duo_mix === true">
                      • Duo_mix
                    </li>
                    <li v-if="rec.features.family_mix === true">
                      • Family Mix
                    </li>
                    <li v-if="rec.features.parental_controls === true">
                      • Parental Controls
                    </li>
                  </ul>
              </div>
            </div>
          </div>
        </div>
        <div class="mb-8 p-6 bg-white rounded-lg shadow-md">
          <h2 class="text-2xl font-bold mb-4">Your Subscriptions</h2>
          <div v-if="loading" class="text-center py-4">
            <p>Loading subscriptions...</p>
          </div>
          <div v-else-if="subscriptions.length" class="space-y-4">
            <div v-for="sub in subscriptions" :key="sub.subscription_id"
                 class="p-4 border rounded-lg hover:shadow-md transition-shadow">
              <div class="flex justify-between items-start">
                <div class="space-y-2">
                  <p class="text-lg font-semibold">{{ sub.plan.provider_name }}</p>
                  <h3 class="text-gray-600">Plan: {{ sub.plan.plan_name }}</h3>
                  <p class="text-gray-600">Status: <span class="font-medium">{{ sub.status }}</span></p>
                  <p class="text-gray-600">Start Date: {{ formatDate(sub.start_date) }}</p>
                  <p class="text-gray-600">Next Billing: {{ formatDate(sub.next_billing_date) }}</p>
                  <p class="text-gray-600">Monthly Fee: ${{ sub.plan.monthly_fee }}</p>
                  <p class="text-gray-600">Auto Renewal:
                    <span class="font-medium">{{ sub.auto_renewal ? 'Enabled' : 'Disabled' }}</span>
                  </p>
                </div>
                <div class="space-y-2">
                  <button
                    @click="cancelSubscription(sub.subscription_id)"
                    class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 transition-colors"
                    :disabled="sub.status !== 'active'"
                  >
                    Cancel Subscription
                  </button>
                  <button
                    v-if="isExtendable(sub)"
                    @click="extendSubscription(sub.subscription_id)"
                    class="block mt-2 bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors"
                  >
                    Extend Subscription
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="text-center py-4">
            <p class="text-gray-600">You don't have any active subscriptions.</p>
            <button
              @click="goToPlans"
              class="mt-4 bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 transition-colors"
            >
              Browse Plans
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Success Notification -->
    <div v-if="notification.show"
         class="fixed top-5 right-5 bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded shadow-md z-50">
      <div class="flex items-center">
        <div class="py-1">
          <svg class="h-6 w-6 text-green-500 mr-4" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
               stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
          </svg>
        </div>
        <div>
          <p class="font-bold">Success!</p>
          <p class="text-sm">{{ notification.message }}</p>
        </div>
        <button @click="closeNotification" class="ml-auto">
          <span class="text-green-500 hover:text-green-700">&times;</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, onMounted} from 'vue';
import {useRouter} from 'vue-router';
import {subAPI, recommendAPI} from '@/api/axios';

export default {
  name: 'UserSubscriptions',
  setup() {
    const router = useRouter();
    const subscriptions = ref([]);
    const recommendations = ref([]);
    const loading = ref(true);
    const notification = ref({
      show: false,
      message: '',
      timer: null
    });

    const showNotification = (message) => {
      // Clear any existing timer
      if (notification.value.timer) {
        clearTimeout(notification.value.timer);
      }

      // Show the notification with the message
      notification.value.show = true;
      notification.value.message = message;

      // Set a timer to hide the notification after 5 seconds
      notification.value.timer = setTimeout(() => {
        notification.value.show = false;
      }, 5000);
    };

    const closeNotification = () => {
      notification.value.show = false;
      if (notification.value.timer) {
        clearTimeout(notification.value.timer);
      }
    };

    const fetchRecommends = async () => {
      try {
        const response = await recommendAPI.post('/recommend', {});
        recommendations.value = response.data.recommends;
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      }
    };

    const fetchSubscriptions = async () => {
      try {
        const response = await subAPI.get('/sub/plans/user');
        subscriptions.value = response.data;
      } catch (error) {
        console.error('Error fetching subscriptions:', error);
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    };

    const isExtendable = (subscription) => {
      if (!subscription.next_billing_date || subscription.status !== 'active') return false;
      const nextBillingDate = new Date(subscription.next_billing_date);
      const today = new Date();
      return nextBillingDate <= today;
    };

    const extendSubscription = async (subscriptionId) => {
      if (!confirm('Would you like to extend this subscription for one more month?')) return;
      try {
        await subAPI.post(`/sub/${subscriptionId}/extend`, {});
        await fetchSubscriptions();
        showNotification('Subscription has been successfully extended.');
      } catch (error) {
        console.error('Error extending subscription:', error);
      }
    };

    const cancelSubscription = async (subscriptionId) => {
      if (!confirm('Are you sure you want to cancel this subscription?')) return;
      try {
        await subAPI.post(`/sub/${subscriptionId}/cancel`, {});
        await fetchSubscriptions();
        showNotification('Subscription has been successfully cancelled.');
      } catch (error) {
        console.error('Error canceling subscription:', error);
      }
    };

    const goToPlans = () => {
      router.push('/plans');
    };

    onMounted(async () => {
      loading.value = true;
      try {
        await Promise.all([fetchSubscriptions(), fetchRecommends()]);
      } catch (error) {
        console.error("Error fetching data:", error);
      } finally {
        loading.value = false;
      }
    });

    return {
      subscriptions,
      recommendations,
      loading,
      notification,
      formatDate,
      cancelSubscription,
      extendSubscription,
      isExtendable,
      goToPlans,
      showNotification,
      closeNotification
    };
  }
};
</script>