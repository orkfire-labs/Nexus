// Java 21 (OpenJDK, default G1 GC) — BigInteger, class-based trees
import java.math.BigInteger;

public class Bench {
    static final long MOD = 1_000_000_007L;

    static long factmod(long n) {
        long r = 1;
        for (long i = 1; i <= n; i++) r = (r * i) % MOD;
        return r;
    }

    static long bigfact(long n) {
        BigInteger r = BigInteger.ONE;
        for (long i = 2; i <= n; i++) r = r.multiply(BigInteger.valueOf(i));
        return r.bitLength();
    }

    static long fib(int n) { return n < 2 ? n : fib(n - 1) + fib(n - 2); }

    static final class Node {
        final Node l, r;
        Node(Node l, Node r) { this.l = l; this.r = r; }
    }

    static Node make(int d) { return d > 0 ? new Node(make(d - 1), make(d - 1)) : new Node(null, null); }

    static long check(Node n) { return n.l == null ? 1 : 1 + check(n.l) + check(n.r); }

    static long trees(int maxd) {
        Node keep = make(maxd);
        long total = 0;
        for (int d = 4; d <= maxd; d += 2) {
            long it = 1L << (maxd - d + 4);
            for (long i = 0; i < it; i++) total += check(make(d));
        }
        return total + check(keep);
    }

    static long sieve(int n) {
        boolean[] s = new boolean[n + 1];
        java.util.Arrays.fill(s, 2, n + 1, true);
        for (long i = 2; i * i <= n; i++)
            if (s[(int) i]) for (long j = i * i; j <= n; j += i) s[(int) j] = false;
        long c = 0;
        for (boolean v : s) if (v) c++;
        return c;
    }

    public static void main(String[] a) {
        String w = a[0];
        long n = a.length > 1 ? Long.parseLong(a[1]) : 0;
        long out = switch (w) {
            case "factmod" -> factmod(n);
            case "bigfact" -> bigfact(n);
            case "fib" -> fib((int) n);
            case "trees" -> trees((int) n);
            case "sieve" -> sieve((int) n);
            default -> 0;
        };
        System.out.println(out);
    }
}
