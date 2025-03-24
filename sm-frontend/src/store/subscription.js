import { defineStore } from 'pinia'
import { subAPI } from '@/api/axios'

export const useSubscriptionStore = defineStore('subscription', {
  state: () => ({
    subscriptions: [],
    activeSubscription: null,
  }),

  actions: {
    async fetchUserSubscriptions(activeOnly = false) {
      try {
        const url = activeOnly ? '/sub/user?status=active' : '/sub/user'
        const response = await subAPI.get(url)
        this.subscriptions = response.data
        if (activeOnly && response.data.length > 0) {
          this.activeSubscription = response.data[0]
        }
      } catch (error) {
        console.error('Failed to fetch subscriptions:', error)
      }
    },

    async createSubscription(subscriptionData) {
      try {
        await subAPI.post('/sub', subscriptionData)
        await this.fetchUserSubscriptions(true)
        return true
      } catch (error) {
        console.error('Failed to create subscription:', error)
        return false
      }
    },

    async cancelSubscription(subscriptionId) {
      try {
        await subAPI.post(`/sub/${subscriptionId}/cancel`)
        await this.fetchUserSubscriptions(true)
        return true
      } catch (error) {
        console.error('Failed to cancel subscription:', error)
        return false
      }
    }
  }
})
