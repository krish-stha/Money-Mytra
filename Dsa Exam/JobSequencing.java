import java.util.Arrays;

class Job {
    int id, deadline, profit;

    public Job(int id, int deadline, int profit) {
        this.id = id;
        this.deadline = deadline;
        this.profit = profit;
    }
}

public class JobSequencing {
    static int jobScheduling(Job[] jobs) {
        // Sort jobs in descending order of profit
        Arrays.sort(jobs, (a, b) -> b.profit - a.profit);

        // Find the maximum deadline to create the scheduling array
        int maxDeadline = 0;
        for (Job job : jobs) {
            maxDeadline = Math.max(maxDeadline, job.deadline);
        }

        // Create an array to store scheduled jobs
        int[] slot = new int[maxDeadline + 1]; 
        Arrays.fill(slot, -1); 

        int totalProfit = 0;
        int countJobs = 0;

        // Iterate through all jobs
        for (Job job : jobs) {
            // Find a slot for the job before its deadline
            for (int j = job.deadline; j > 0; j--) {
                if (slot[j] == -1) {  // If slot is free
                    slot[j] = job.id; // Assign the job
                    totalProfit += job.profit; 
                    countJobs++; 
                    break;
                }
            }
        }
        
        System.out.println("Total Jobs Done: " + countJobs);
        return totalProfit;
    }

    public static void main(String[] args) {
        Job[] jobs = {
            new Job(1, 5, 15),
            new Job(2, 2, 10),
            new Job(3, 3, 12),
            new Job(4, 1, 20),
            new Job(5, 3, 8)
        };

        int maxProfit = jobScheduling(jobs);
        System.out.println("Maximum Profit: " + maxProfit);
    }
}
