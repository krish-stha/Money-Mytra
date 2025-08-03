// import java.util.Stack;

// class Queue{
//     private Stack <Integer> Stack1; // for enqueue
//     private Stack <Integer> Stack2; // for dequeue

//     // making a constructor
//     Queue(){
//         Stack1 = new Stack<>();
//         Stack2 = new Stack<>();
//     }

//     // Enqueue Operation
//     void Enqueue(int n){
//         Stack1.push(n); // pushing the element in Stack1
//     }

//     // Dequeue Operation
//     public int dequeue(){
//         if(Stack2.isEmpty()){
//             while(!Stack1.isEmpty()){
//                 Stack2.push(Stack1.pop());
//             }
//         }

//         if(Stack2.isEmpty()){
//             System.out.println("Queue is Empty");
//             return -1;
//         }
//         return Stack2.pop();
//     }

//     public boolean isEmpty(){
//         return Stack1.isEmpty() && Stack2.isEmpty();
//     }

//     public int front(){
//         if(Stack2.isEmpty()){
//             while(!Stack1.isEmpty()){
//                 Stack2.push(Stack1.pop());
//             }
//         }
//         if(Stack2.isEmpty()){
//             System.out.println("Queue is Empty");
//             return -1;
//         }
//         return Stack2.peek();
//     }

//     public int rear(){
//         // If Stack1 is not empty, the rear element is the top of Stack1
//         if (!Stack1.isEmpty()){
//             return Stack1.peek();
//         } 
        
//         // If Stack1 is empty, the rear is the last item popped into Stack2
//         if (!Stack2.isEmpty()){
//             return Stack2.firstElement(); // Get the first element that was added to Stack2
//         }

//         System.out.println("Queue is Empty");
//         return -1;
//     }
// }

// public class QueueStack{
//     public static void main (String[] args){

//         Queue queue = new Queue();

//         queue.Enqueue(5);
//         queue.Enqueue(6);
//         queue.Enqueue(7);
//         queue.Enqueue(8);

//         System.out.println("The first item is " + queue.front()); // Expected 5
//         System.out.println("The last item is " + queue.rear()); // Expected 8

//         queue.dequeue(); // Removing 5

//         System.out.println("The first item is " + queue.front()); // Expected 6
//         System.out.println("The last item is " + queue.rear()); // Expected 8
//     }
// }


import java.util.Stack;
class Queue{
    private Stack<Integer> Stack1;
    private Stack<Integer> Stack2;

    Queue(){
        Stack1=new Stack<>();
        Stack2=new Stack<>();
    }

    //for enqueue

    void enqueue(int n){
        Stack1.push(n);
    }

    //for dequeue

    int dequeue(){
        if(Stack2.isEmpty()){
            while(!Stack1.isEmpty()){
                Stack2.push(Stack1.pop());
            }
        }
        if(Stack2.isEmpty()){
            System.out.println("Queue is Empty");
            return -1;
        } 
        return Stack2.pop(); 
    }

    // for front 
    int front(){
        if(Stack2.isEmpty()){
            while(!Stack1.isEmpty()){
                Stack2.push(Stack1.pop());
            }
        }

        if(Stack2.isEmpty()){
            System.out.println("Queue is Empty");
            return -1;
        }
        return Stack2.peek();

    }


    //for rear
    int rear(){
        if(!Stack1.isEmpty()){
            return Stack1.peek();
        }

        if(!Stack2.isEmpty()){
            return Stack2.firstElement();
        }

        System.out.println("Queue is Empty");
        return -1;
    }

}
    
    


public class QueueStack{
    public static void main (String[] args){
        Queue queue = new Queue();

                queue.enqueue(5);
                queue.enqueue(6);
                queue.enqueue(7);
                queue.enqueue(8);
        
                System.out.println("The first item is " + queue.front()); // Expected 5
                System.out.println("The last item is " + queue.rear()); // Expected 8
        
                queue.dequeue(); // Removing 5
        
                System.out.println("The first item is " + queue.front()); // Expected 6
                System.out.println("The last item is " + queue.rear()); // Expected 8

    }
}