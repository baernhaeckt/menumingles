using backend.Discussion.Storage;

using System.Text.Json;

namespace backend.Discussion.Api;

public record DiscussionResultResponse(MenuResultStatus Status, JsonDocument Result);