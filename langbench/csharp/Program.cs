// C# / .NET 8 (Release, default workstation GC, Tiered PGO on) — System.Numerics.BigInteger, class trees
using System.Numerics;

const ulong MOD = 1_000_000_007UL;

ulong FactMod(ulong n)
{
    ulong r = 1;
    for (ulong i = 1; i <= n; i++) r = (r * i) % MOD;
    return r;
}

long BigFact(long n)
{
    BigInteger r = BigInteger.One;
    for (long i = 2; i <= n; i++) r *= i;
    return (long)r.GetBitLength();
}

long Fib(int n) => n < 2 ? n : Fib(n - 1) + Fib(n - 2);

long Trees(int maxd)
{
    var keep = Node.Make(maxd);
    long total = 0;
    for (int d = 4; d <= maxd; d += 2)
    {
        long it = 1L << (maxd - d + 4);
        for (long i = 0; i < it; i++) total += Node.Make(d).Check();
    }
    return total + keep.Check();
}

long Sieve(int n)
{
    var s = new bool[n + 1];
    Array.Fill(s, true, 2, n - 1);
    for (long i = 2; i * i <= n; i++)
        if (s[i]) for (long j = i * i; j <= n; j += i) s[j] = false;
    long c = 0;
    foreach (var v in s) if (v) c++;
    return c;
}

var w = args[0];
long n = args.Length > 1 ? long.Parse(args[1]) : 0;
long output = w switch
{
    "factmod" => (long)FactMod((ulong)n),
    "bigfact" => BigFact(n),
    "fib" => Fib((int)n),
    "trees" => Trees((int)n),
    "sieve" => Sieve((int)n),
    _ => 0,
};
Console.WriteLine(output);

sealed class Node
{
    public readonly Node? L, R;
    Node(Node? l, Node? r) { L = l; R = r; }
    public static Node Make(int d) => d > 0 ? new Node(Make(d - 1), Make(d - 1)) : new Node(null, null);
    public long Check() => L is null ? 1 : 1 + L.Check() + R!.Check();
}
