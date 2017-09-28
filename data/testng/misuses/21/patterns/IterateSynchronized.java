import org.testng.ISuite;
import org.testng.ISuiteResult;
import org.testng.ITestContext;

import java.util.Map;

class IterateSynchonized {  
  ITestContext pattern(ISuite suite) {
    // This invokation (may?) return a synchronized map.
    Map<String, ISuiteResult> suiteResults = suite.getResults();
    synchronized(suiteResults) {
      for (ISuiteResult sr : suiteResults.values()) {
        ITestContext context = sr.getTestContext();
        return context; // do something with context
      }
    }
    return null;
  }
}
