import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;

class FlushStreamBeforeGetBytes474 {
  byte[] pattern(OutputStream out) throws IOException {
    DataOutputStream dout = new DataOutputStream(out);
    dout.writeInt(0);
    dout.flush();
  }
}
