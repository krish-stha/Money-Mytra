import java.util.*;

public class KEvenMixedSort {
    public static void sortKEvenMixedArray(int[] A) {
        List<Integer> evenNumbers = new ArrayList<>();
        List<Integer> evenIndices = new ArrayList<>();

        // Extract even numbers and their positions
        for (int i = 0; i < A.length; i++) {
            if (A[i] % 2 == 0) {
                evenNumbers.add(A[i]);
                evenIndices.add(i);
            }
        }

        // Sort the even numbers
        Collections.sort(evenNumbers);

        // Put the sorted even numbers back in their original positions
        for (int i = 0; i < evenNumbers.size(); i++) {
            A[evenIndices.get(i)] = evenNumbers.get(i);
        }
    }
    public static void main(String[] args) {
        int[] A = {3, 8, 5, 2, 7, 6, 11, 4}; // Example k even mixed array
        sortKEvenMixedArray(A);
        System.out.println(Arrays.toString(A)); // Output: [3, 2, 5, 4, 7, 6, 11, 8]
    }
}

// import java.util.*;

// public class KEvenMixedSort{
//     public static void KSort(int[] arr){
//         List <Integer> evenNum=new ArrayList<>();
//         List <Integer> evenindex=new ArrayList<>();

//         for(int i=0; i<=arr.length;i++){
//             if(arr[i]%2==0){
//                 evenNum.add(arr[i]);
//                 evenindex.add(i);
//             }
//         }

//         Collections.sort(evenNum);

//         for(int i=0;i<evenNum.size();i++){   
//             arr[evenindex.get(i)]=evenNum.get(i);
//         }
//     }
// }


