namespace backend.Planning.Api;

public class PlanningStartRequest
{
    public required IEnumerable<string> Ingredients { get; set; }
}
