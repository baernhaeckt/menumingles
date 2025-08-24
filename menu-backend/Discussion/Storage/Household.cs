using System.Text.Json;

namespace backend.Discussion.Storage;

public class Household
{
    public string HouseholdKey { get; set; } = string.Empty;

    public string Name { get; set; } = string.Empty;

    public required JsonDocument People { get; set; }

    public required JsonDocument Chef { get; set; }

    public required JsonDocument Consultants { get; set; }
}