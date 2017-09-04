import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;

class FlushStreamBeforeGetBytes {
  byte[] pattern(long l) {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    DataOutputStream dos = new DataOutputStream(baos);
    try {
      dos.writeLong(l);
      dos.flush();
    } catch (IOException e) {
      return new byte[0];
    }
    return baos.toByteArray();
  }
}
