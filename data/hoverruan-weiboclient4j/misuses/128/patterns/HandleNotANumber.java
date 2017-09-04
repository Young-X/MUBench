import weiboclient4j.params.Cid;

class HandleNotANumber {
  Cid cid(String value) {
    try {
      // The constructor invokes Long.parseLong() on the string parameter.
      return new Cid(value);
    } catch (NumberFormatException e) {
      throw new NumberFormatException(String.format("Cid value [%s] is not a parseable Long", value));
    }
  }
}
