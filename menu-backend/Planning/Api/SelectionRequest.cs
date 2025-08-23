namespace backend.Planning.Api;

public class SelectionRequest
{
    public string SessionKey { get; set; }

    public IEnumerable<string> MatchedMenus { get; set; }
}
