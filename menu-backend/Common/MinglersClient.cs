using Microsoft.Extensions.Primitives;

using System.Text.Json;

namespace backend.Common;

public class MenuMinglersClient
{
    private readonly HttpClient _http;

    public MenuMinglersClient(HttpClient http)
    {
        _http = http ?? throw new ArgumentNullException(nameof(http));
    }

    /// <summary>POST /api/v1/discuss</summary>
    public async Task<DiscussionResponse?> DiscussAsync(DiscussionRequest request, CancellationToken ct = default)
    {
        var response = await _http.PostAsJsonAsync("/api/v1/discuss", request, ct);

        if (response.StatusCode == System.Net.HttpStatusCode.UnprocessableEntity)
        {
            var error = await response.Content.ReadFromJsonAsync<HTTPValidationError>(cancellationToken: ct);
            throw new ValidationException(error);
        }

        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<DiscussionResponse>(cancellationToken: ct);
    }

    /// <summary>POST /api/v1/discuss</summary>
    public async Task BroadcastMessageAsync(BroadcastRequest request, CancellationToken ct = default)
    {
        var response = await _http.PostAsJsonAsync("/api/v1/ws/broadcast", request, ct);
        response.EnsureSuccessStatusCode();
    }
}

/// <summary>
/// Root request for /api/v1/discuss
/// </summary>
public sealed record DiscussionRequest(
    JsonDocument People,
    JsonDocument Chef,
    JsonDocument Consultants,
    JsonElement[] Menu
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
