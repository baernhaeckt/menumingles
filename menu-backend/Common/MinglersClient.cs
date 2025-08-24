using Microsoft.Extensions.Primitives;

using System.Text.Json;
using System.Text.Json.Serialization;

namespace backend.Common;

public class MenuMinglersClient
{
    private readonly HttpClient _http;

    public MenuMinglersClient(HttpClient http)
    {
        _http = http ?? throw new ArgumentNullException(nameof(http));
    }

    /// <summary>POST /api/v1/discuss</summary>
    public async Task<DiscussionTaskResponse?> DiscussAsync(DiscussionRequest request, CancellationToken ct = default)
    {
        HttpResponseMessage response = await _http.PostAsJsonAsync("/api/v1/discuss", request, ct);

        if (response.StatusCode == System.Net.HttpStatusCode.UnprocessableEntity)
        {
            HTTPValidationError? error = await response.Content.ReadFromJsonAsync<HTTPValidationError>(cancellationToken: ct);
            throw new ValidationException(error);
        }

        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<DiscussionTaskResponse>(cancellationToken: ct);
    }

    /// <summary>
    /// GET /api/v1/discuss/{task_id}/status – poll discussion status/results
    /// </summary>
    public async Task<DiscussionStatusResponse?> GetDiscussionStatusAsync(string taskId, CancellationToken ct = default)
    {
        HttpResponseMessage response = await _http.GetAsync($"/api/v1/discuss/{taskId}/status", ct);

        if (response.StatusCode == System.Net.HttpStatusCode.UnprocessableEntity)
        {
            HTTPValidationError? error = await response.Content.ReadFromJsonAsync<HTTPValidationError>(cancellationToken: ct);
            throw new ValidationException(error);
        }

        if (response.StatusCode == System.Net.HttpStatusCode.NotFound)
        {
            return null;
        }

        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<DiscussionStatusResponse>(cancellationToken: ct);
    }

    /// <summary>POST /api/v1/discuss</summary>
    public async Task BroadcastMessageAsync(BroadcastRequest request, CancellationToken ct = default)
    {
        HttpResponseMessage response = await _http.PostAsJsonAsync("/api/v1/ws/broadcast", request, ct);
        response.EnsureSuccessStatusCode();
    }
}

/// <summary>
/// Response for polling discussion task status
/// </summary>
public sealed record DiscussionStatusResponse(
    [property: JsonPropertyName("task_id")] string TaskId,
    [property: JsonPropertyName("status")] string Status,
    [property: JsonPropertyName("created_at")] DateTime CreatedAt,
    [property: JsonPropertyName("started_at")] DateTime? StartedAt,
    [property: JsonPropertyName("completed_at")] DateTime? CompletedAt,
    [property: JsonPropertyName("result")] JsonElement? Result,
    [property: JsonPropertyName("error")] string? Error
);
/// <summary>
/// Root request for /api/v1/discuss
/// </summary>
public sealed record DiscussionRequest(
    JsonDocument People,
    JsonDocument Chef,
    JsonDocument Consultants,
    JsonElement[] Menu
);
/// <summary>
/// Response when starting async discussion
/// </summary>
public sealed record DiscussionTaskResponse(
    [property: JsonPropertyName("task_id")] string TaskId,
    [property: JsonPropertyName("status")] string Status,
    [property: JsonPropertyName("message")] string Message
);

public sealed record DiscussionResponse(
    JsonElement[] Results // schema not fixed. Contains weekdays
);


/// <summary>
/// Root request for /api/v1/ws/broadcast
/// </summary>
public sealed record BroadcastRequest(
    string Type,
    string Name,
    string Message
);
