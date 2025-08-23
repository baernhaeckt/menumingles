using System.Text.Json;

namespace backend.Planning.Storage;

public class Session
{
    public string SessionKey { get; set; }

    public string HouseholdKey { get; set; }

    public IEnumerable<string> MatchedMenus { get; set; }

    public JsonDocument MenuSelection { get; set; }
}