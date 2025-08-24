using System.Text.Json;

namespace backend.Discussion.Storage;

public class MenuResult
{
    public MenuResultStatus Status { get; set; }

    public JsonDocument? Result { get; set; }

    public string TaskId { get; internal set; }
}