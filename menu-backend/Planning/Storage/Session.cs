using System.Text.Json;

namespace backend.Planning.Storage;

public class Session
{
    public string SessionKey { get; set; } = string.Empty;

    public string HouseholdKey { get; set; } = string.Empty;

    public IEnumerable<string> MatchedMenus { get; set; } = Enumerable.Empty<string>();

    public required JsonDocument MenuSelection { get; set; }
}