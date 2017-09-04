import java.util.List;
import java.util.ArrayList;

import org.testng.ITestContext;
import org.testng.internal.Utils;

class IterateSynchonized {
  private List<ITestContext> syncL = Collections.synchronizedList(new ArrayList<ITestContext>());
  
  void pattern() {
    synchronized(syncL) {
      for (ITestContext tr : syncL) {
        long elapsedTimeMillis= tr.getEndMillis() - tr.getStartMillis();
        String name= tr.getMethod().isTest() ? tr.getName() : Utils.detailedMethodName(tr.getMethod(), false);
      }
    }
  }
}
