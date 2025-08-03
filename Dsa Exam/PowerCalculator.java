public class PowerCalculator {
    
    // Function to calculate power using divide and conquer
    public static long power(int base, int exponent) {
        if (exponent == 0) return 1;  // Base case: x^0 = 1
        if (exponent == 1) return base; // Base case: x^1 = x
        
        long halfPower = power(base, exponent / 2); // Divide

        if (exponent % 2 == 0) {
            return halfPower * halfPower; // Even case: x^n = (x^(n/2))^2
        } else {
            return base * halfPower * halfPower; // Odd case: x^n = x * (x^(n/2))^2
        }
    }

    public static void main(String[] args) {
        int base = 3;
        int exponent = 5;
        System.out.println(base + "^" + exponent + " = " + power(base, exponent));
    }
}
