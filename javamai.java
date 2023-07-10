import javax.mail.Session;
public class CheckJavaMailInstallation {
    public static void main(String[] args) {
        Session session = Session.getDefaultInstance(System.getProperties());
        System.out.println("Java Mail version: " + session.getProperty("mail.version"));
    }
}