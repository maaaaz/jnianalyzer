public class Test {
    public static void main(String[] args) {
        System.load(System.getProperty("user.dir") + "/secretcode.so");
        System.out.println(SecretCode.encode(args[0]));
    }
}
