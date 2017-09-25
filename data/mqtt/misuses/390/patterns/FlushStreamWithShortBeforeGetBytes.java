import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;

class FlushStreamWithShortBeforeGetBytes {
  byte[] pattern(short s) {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    DataOutputStream dos = new DataOutputStream(baos);
    try {
      dos.writeShort(s);
      dos.flush();
      return baos.toByteArray();
    } catch (IOException e) {
      return new byte[0];
    }
  }
}
