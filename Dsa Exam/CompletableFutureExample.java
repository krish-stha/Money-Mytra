import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;


public class CompletableFutureExample{
    public static void main(String[] args) throws ExecutionException,InterruptedException{
        //task 1

        CompletableFuture<Integer> task1=CompletableFuture.supplyAsync(() -> {
            System.out.println("Task 1 started");
            try{
                Thread.sleep(3000);
            }catch(InterruptedException e){
                e.printStackTrace();
            }
            return 20;
        });

        CompletableFuture <Integer>task2=CompletableFuture.supplyAsync(()->{
            System.out.println("task2 is stated");
            try {
                Thread.sleep(2000);
                
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            return 50;
        });

         // Combine results of both tasks
//         CompletableFuture<Integer> combinedResult = task1.thenCombine(task2, (result1, result2) -> {
//             System.out.println("Combining the results...");
//             return result1 + result2; // Combine the results
//         });

//         // Wait and get the combined result
//         Integer finalResult = combinedResult.get(); // Blocks and waits for the result

//         // Print the final result
//         System.out.println("Final result: " + finalResult);

        CompletableFuture <Integer> combinedResult=task1.thenCombine(task2, (result1,result2)->{
            System.out.println("combining the resul...t");
            return result1+result2;
        });

        Integer finalResult=combinedResult.get();

        
        System.out.println(finalResult);

    }
}








// import java.util.concurrent.CompletableFuture;
// import java.util.concurrent.ExecutionException;

// public class CompletableFutureExample {

//     public static void main(String[] args) throws ExecutionException, InterruptedException {
        
//         // Task 1: Simulate a task with a delay
//         CompletableFuture<Integer> task1 = CompletableFuture.supplyAsync(() -> {
//             System.out.println("Task 1 is running...");
//             try {
//                 Thread.sleep(2000); // Simulating a delay
//             } catch (InterruptedException e) {
//                 e.printStackTrace();
//             }
//             return 20;
//         });

//         // Task 2: Simulate another task with a delay
//         CompletableFuture<Integer> task2 = CompletableFuture.supplyAsync(() -> {
//             System.out.println("Task 2 is running...");
//             try {
//                 Thread.sleep(1000); // Simulating a delay
//             } catch (InterruptedException e) {
//                 e.printStackTrace();
//             }
//             return 30;
//         });

//         // Combine results of both tasks
//         CompletableFuture<Integer> combinedResult = task1.thenCombine(task2, (result1, result2) -> {
//             System.out.println("Combining the results...");
//             return result1 + result2; // Combine the results
//         });

//         // Wait and get the combined result
//         Integer finalResult = combinedResult.get(); // Blocks and waits for the result

//         // Print the final result
//         System.out.println("Final result: " + finalResult);
//     }
// }
