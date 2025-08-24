namespace backend.Planning.Api;

public class SelectionRequest
{
    public required string SessionKey { get; set; }

    public required IEnumerable<string> MatchedMenus { get; set; }
}
