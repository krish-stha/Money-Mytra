// public class MaxSubarraySum {
//     public static int maxSubArray(int[] nums) {
//         int maxSum = nums[0]; // Initialize maxSum with the first element
//         int currentSum = nums[0]; // Track the current subarray sum

//         for (int i = 1; i < nums.length; i++) {
//             // Either extend the current subarray or start a new one
//             currentSum = Math.max(nums[i], currentSum + nums[i]);
//             maxSum = Math.max(maxSum, currentSum);
//         }

//         return maxSum;
//     }

//Kandanes Algorithm

public class MaxSubarraySum{

    public static int maxSum(int[] num){
        int maxSum=num[0];
        int currentSum=num[0];

        for(int i=1;i<num.length;i++){
            currentSum=Math.max(num[i],currentSum+ num[i]);
            maxSum=Math.max(maxSum,currentSum);
        }
        return maxSum;
    }

    public static void main(String[] args) {
        int[] nums = {-2, 1, -3, 4, -1, 2, 1, -5, 4};
        System.out.println("Maximum Subarray Sum: " + maxSum(nums)); // Output: 6
    }
}
