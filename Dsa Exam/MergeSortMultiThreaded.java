// import java.util.Arrays;

// // Class for multithreaded Merge Sort
// class MergeSortMultiThreaded extends Thread {
//     private int[] array; // The array to be sorted

//     // Constructor to initialize the array
//     public MergeSortMultiThreaded(int[] array) {
//         this.array = array;
//     }

//     // Overriding run() method for the thread's execution
//     @Override
//     public void run() {
//         mergeSort(array); // Start the sorting process
//     }

//     // Merge Sort algorithm (recursive)
//     private void mergeSort(int[] arr) {
//         if (arr.length <= 1) return; // Base condition: single element is already sorted

//         int mid = arr.length / 2; // Find the middle index
//         int[] left = Arrays.copyOfRange(arr, 0, mid); // Left half
//         int[] right = Arrays.copyOfRange(arr, mid, arr.length); // Right half

//         // Create threads to sort left and right halves
//         Thread leftThread = new MergeSortMultiThreaded(left);
//         Thread rightThread = new MergeSortMultiThreaded(right);

//         leftThread.start(); // Start sorting left half in a separate thread
//         rightThread.start(); // Start sorting right half in another thread

//         // Ensure both threads complete before merging
//         try { 
//             leftThread.join(); 
//             rightThread.join(); 
//         } catch (Exception ignored) {}

//         // Merge the sorted halves
//         merge(arr, left, right);
//     }

//     // Merging two sorted halves into a single sorted array
//     private void merge(int[] arr, int[] left, int[] right) {
//         int i = 0, j = 0, k = 0;

//         // Compare elements from both halves and merge in sorted order
//         while (i < left.length && j < right.length)
//             arr[k++] = (left[i] < right[j]) ? left[i++] : right[j++];

//         // Copy remaining elements (if any) from left half
//         while (i < left.length) arr[k++] = left[i++];

//         // Copy remaining elements (if any) from right half
//         while (j < right.length) arr[k++] = right[j++];
//     }

//     // Main method to run the sorting
//     public static void main(String[] args) {
//         int[] array = {38, 27, 43, 3, 9, 82, 10}; // Example array
//         System.out.println("Original Array: " + Arrays.toString(array));

//         // Start sorting in a separate thread
//         Thread sorter = new MergeSortMultiThreaded(array);
//         sorter.start();

//         // Wait for sorting to complete before printing the result
//         try { 
//             sorter.join(); 
//         } catch (Exception ignored) {}

//         System.out.println("Sorted Array: " + Arrays.toString(array));
//     }
// }


// import java.util.Arrays;

// class MergeSortMultiThreaded extends Thread{
//     int[] arr;

//     MergeSortMultiThreaded(int[] arr){
//         this.arr=arr;
//     }

//     @Override

//     public void run(){
//         mergeSort(arr);
//     }

//     private void mergeSort(int[] arr){
//         if(arr.length <=1 ) return;

//         int mid=arr.length/2;
//         int[] left=Arrays.copyOfRange(arr,0,mid);
//         int[] right=Arrays.copyOfRange(arr,mid,arr.length);

//         //creating a thread

//         Thread leftThread=new MergeSortMultiThreaded(left);
//         Thread rightThread=new MergeSortMultiThreaded(right);

//         //starting the thread

//         leftThread.start();
//         rightThread.start();

//         try {
//             leftThread.join();
//             rightThread.join();
            
//         } catch (Exception ignored) {
//         }

//         merge(arr,left,right);
//     }

//     private void merge(int[] arr,int[] left,int[] right){
//         int i=0,j=0,k=0;

//         while (i<left.length && j<right.length)
//         arr[k++]=(left[i]<right[j])?left[i++]:right[j++];

//         while (i<left.length)
//         arr[k++]=left[i++];

//         while (j<right.length)
//         arr[k++]=right[j++];
//     }

//     public static void main (String[] args){
//         int[] array={5,9,8,7,15,9,63};
//         Thread sorter=new MergeSortMultiThreaded(array);
//         sorter.start();

//         try {
//             sorter.join();
            
//         } catch (Exception ignored) {
//         }

//         System.out.println(Arrays.toString(array));
//     }



// }


import java.util.Arrays;

class MergeSortMultiThreaded extends Thread{
    int[] arr;

    public MergeSortMultiThreaded(int[] arr) {
        this.arr=arr;
    }
    
    @Override
    public void run(){
        mergeSort(arr);
    }

    public void mergeSort(int[] array){

        if(array.length<=1) {return;}
        int mid=array.length/2;
        int[] left=Arrays.copyOfRange(array,0,mid);
        int[] right=Arrays.copyOfRange(array,mid,array.length);

        //making a thread


        Thread leftThread=new MergeSortMultiThreaded(left);
        Thread rightThread=new MergeSortMultiThreaded(right);

        //starting the thread

        leftThread.start();
        rightThread.start();

        try {
            leftThread.join();
            rightThread.join();
            
        } catch (Exception ignored) {
        }

        merge(array,left,right);


    }

    void merge(int[] arr, int[] left, int[] right){
        int i = 0, j = 0, k = 0;

        while(i<left.length && j<right.length)

        arr[k++]=(left[i]<right[j])?left[i++]:right[j++];

        while (i<left.length)
        arr[k++]=left[i++];

        while(j<right.length)
        arr[k++]=right[j++];



    }

    public static void main(String[] args){

        int[] array={2,78,5,69,32,10,5,3,8};

        Thread sorter=new MergeSortMultiThreaded(array);

        sorter.start();

        try {
            sorter.join();
            
        } catch (Exception ignored) {
        }

        System.out.println(Arrays.toString(array));

    }
    
}
