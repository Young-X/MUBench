import java.io.DataOutputStream;
import java.io.IOException;
import java.io.OutputStream;

class FlushStreamBeforeGetBytes {
  byte[] pattern(OutputStream out) throws IOException {
      DataOutputStream dout = new DataOutputStream(out);
      dout.writeInt(0);
      dout.flush();
    }
  }
}
