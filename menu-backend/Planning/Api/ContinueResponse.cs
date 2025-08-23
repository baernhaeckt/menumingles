using System.Text.Json;

namespace backend.Planning.Api;

public class ContinueResponse
{
    public string SessionKey { get; set; }

    public JsonDocument MenuSelection { get; set; }
}
