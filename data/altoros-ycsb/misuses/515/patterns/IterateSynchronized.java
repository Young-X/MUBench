import java.util.List;
import java.util.ArrayList;

import org.testng.ITestContext;
import org.testng.internal.Utils;

class IterateSynchonized {
  private List<ITestContext> syncL = Collections.synchronizedList(new ArrayList<ITestContext>());
  
  long pattern() {
    synchronized(syncL) {
      for (ITestContext tr : syncL) {
        return tr.getEndMillis() - tr.getStartMillis(); // do something with tr
      }
    }
  }
}
