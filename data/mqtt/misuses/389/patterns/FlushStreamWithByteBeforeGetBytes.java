import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;

class FlushStreamWithByteBeforeGetBytes {
  byte[] pattern(byte b) {
    ByteArrayOutputStream baos = new ByteArrayOutputStream();
    DataOutputStream dos = new DataOutputStream(baos);
    try {
      dos.writeByte(b);
      dos.flush();
      return baos.toByteArray();
    } catch (IOException e) {
      return new byte[0];
    }
  }
}
