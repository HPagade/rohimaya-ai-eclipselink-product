import Layout from '@/components/Layout'
import { useAuthStore } from '@/store/authStore'

export default function Rewards() {
  const user = useAuthStore(state => state.user)

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-6">Phoenix & Peacock Honors™</h1>
        
        <div className="bg-gradient-to-r from-phoenix-orange-500 to-peacock-teal-500 text-white rounded-lg shadow-lg p-8 mb-6">
          <div className="text-center">
            <div className="text-6xl font-bold mb-2">0</div>
            <div className="text-xl">Total Points Earned</div>
            <div className="text-sm opacity-90 mt-2">{user?.first_name}, start earning points by creating handoffs!</div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">How to Earn Points</h2>
          <div className="space-y-4">
            <div className="flex items-start">
              <div className="w-12 h-12 bg-peacock-teal-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-2xl">📋</span>
              </div>
              <div>
                <div className="font-medium">Complete a Baseline Handoff</div>
                <div className="text-sm text-gray-600">Earn 10 points for each new patient handoff</div>
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-12 h-12 bg-lunar-blue-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-2xl">🔄</span>
              </div>
              <div>
                <div className="font-medium">Update-Only Handoff</div>
                <div className="text-sm text-gray-600">Earn 5 points for quick updates</div>
              </div>
            </div>
            <div className="flex items-start">
              <div className="w-12 h-12 bg-phoenix-orange-100 rounded-full flex items-center justify-center mr-4">
                <span className="text-2xl">🚨</span>
              </div>
              <div>
                <div className="font-medium">Critical Alert Detection</div>
                <div className="text-sm text-gray-600">Earn 15 bonus points for flagging critical issues</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}
