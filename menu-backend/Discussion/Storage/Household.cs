using System.Text.Json;

namespace backend.Discussion.Storage;

public class Household
{
    public string HouseholdKey { get; set; } = string.Empty;

    public string Name { get; set; } = string.Empty;

    public JsonDocument People { get; set; }

    public JsonDocument Chef { get; set; }

    public JsonDocument Consultants { get; set; }
}