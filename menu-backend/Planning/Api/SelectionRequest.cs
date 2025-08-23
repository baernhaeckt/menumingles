using System.Text.Json;

namespace backend.Planning.Api;

public class SelectionRequest
{
    public string SessionKey { get; set; }

    public JsonDocument MatchedMenus { get; set; }
}
