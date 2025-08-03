public class MaxElement {
    public static int findMax(int[] arr) {
        int max = arr[0]; // Start with the first element as max

        for (int num : arr) { // Loop through each element
            if (num > max) {
                max = num; // Update max if a larger value is found
            }
        }

        return max; // Return the largest element
    }

    public static void main(String[] args) {
        int[] arr = {3, 10, 2, 50, 7, 8, 100, 45}; // Example array

        System.out.println("Maximum element is: " + findMax(arr)); // Print result
    }
}

