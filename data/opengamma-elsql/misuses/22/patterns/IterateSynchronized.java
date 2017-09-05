import org.testng.ISuite;
import org.testng.ISuiteResult;
import org.testng.ITestContext;

import java.util.Map;

class IterateSynchonized {  
  ITestContext pattern(ISuite suite) {
    // This invokation (may?) return a synchronized map.
    Map<String, ISuiteResult> results = suite.getResults();
    synchronized(results) {
      for (Map.Entry<String, ISuiteResult> result : results.entrySet()) {
        ITestContext testContext = result.getValue().getTestContext();
        return context; // do something with context
      }
    }
    return null;
  }
}
