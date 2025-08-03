public class MaxHeap {

    public static void heapify(int[] arr, int n , int i){
        int largest=i;
        int left=2*i+1;
        int right=2*i+2;


        while(left<n){

            if(left<n && arr[left]>arr[largest]){
                largest=left;
            }

            if(right<n && arr[right]>arr[largest]){
                largest=right;
            }

            if(largest!=i){
                int temp=arr[i];
                arr[i]=arr[largest];
                arr[largest]=temp;

                i=largest;
                left=2*i+1;
                right=2*i+2;


            }else{
                break;
            }
        }
    }
    
}
