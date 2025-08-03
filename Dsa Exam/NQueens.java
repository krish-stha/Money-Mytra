class NQueens {
    static int N = 4; // Change N to solve for different board sizes

    // Function to print the board
    static void printBoard(int board[][]) {
        for (int i = 0; i < N; i++) {
            for (int j = 0; j < N; j++) {
                System.out.print(board[i][j] == 1 ? "Q " : ". ");
            }
            System.out.println();
        }
        System.out.println();
    }

    // Check if it's safe to place a queen at board[row][col]
    static boolean isSafe(int board[][], int row, int col) {
        // Check column (above rows)
        for (int i = 0; i < row; i++)
            if (board[i][col] == 1)
                return false;

        // Check upper-left diagonal
        for (int i = row, j = col; i >= 0 && j >= 0; i--, j--)
            if (board[i][j] == 1)
                return false;

        // Check upper-right diagonal
        for (int i = row, j = col; i >= 0 && j < N; i--, j++)
            if (board[i][j] == 1)
                return false;

        return true;
    }

    // Backtracking function to solve N-Queens
    static boolean solveNQueens(int board[][], int row) {
        if (row == N) { // All queens placed successfully
            printBoard(board);
            return true;
        }

        boolean success = false;
        for (int col = 0; col < N; col++) {
            if (isSafe(board, row, col)) {
                board[row][col] = 1; // Place the queen

                // Recur for the next row
                success = solveNQueens(board, row + 1) || success;

                // Backtrack (remove the queen)
                board[row][col] = 0;
            }
        }
        return success;
    }

    public static void main(String[] args) {
        int board[][] = new int[N][N];

        if (!solveNQueens(board, 0)) {
            System.out.println("No solution exists");
        }
    }
}
