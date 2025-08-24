using System.Text.Json;

namespace backend.Planning.Api;

public class ContinueResponse
{
    public required string SessionKey { get; set; }

    public required JsonDocument MenuSelection { get; set; }
}
