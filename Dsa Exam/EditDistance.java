public class EditDistance {
    public static int findEditDistance(String str1, String str2) {
        int m = str1.length();
        int n = str2.length();
        
     
        int[][] dp = new int[m + 1][n + 1];

       
        for (int i = 0; i <= m; i++) {
            dp[i][0] = i; // Deleting all characters
        }
        for (int j = 0; j <= n; j++) {
            dp[0][j] = j; // Inserting all characters
        }

        // Fill the DP table
        for (int i = 1; i <= m; i++) {
            for (int j = 1; j <= n; j++) {
                if (str1.charAt(i - 1) == str2.charAt(j - 1)) {
                    dp[i][j] = dp[i - 1][j - 1]; // No change needed
                } else {
                    dp[i][j] = 1 + Math.min(dp[i - 1][j],    // Deletion
                                    Math.min(dp[i][j - 1],    // Insertion
                                             dp[i - 1][j - 1])); // Substitution
                }
            }
        }
        
        return dp[m][n]; // The final edit distance
    }

    public static void main(String[] args) {
        String str1 = "Artificial";
        String str2 = "krish";
        
        System.out.println("Edit Distance: " + findEditDistance(str1, str2));
    }
}
