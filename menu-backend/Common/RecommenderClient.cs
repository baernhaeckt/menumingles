namespace backend.Common;

using System.Net.Http.Json;
using System.Text.Json;

public class RecommenderClient
{
    private readonly HttpClient _http;

    public RecommenderClient(HttpClient http)
    {
        _http = http ?? throw new ArgumentNullException(nameof(http));
    }

    /// <summary>
    /// GET /api/v1/health/ – Health check
    /// </summary>
    public async Task<JsonDocument?> GetHealthAsync(CancellationToken ct = default)
    {
        var response = await _http.GetAsync("/api/v1/health/", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<JsonDocument>(cancellationToken: ct);
    }

    /// <summary>
    /// POST /api/v1/menu/recommender – Inventory Recommender
    /// </summary>
    /// <param name="ingredients">Array of ingredient strings</param>
    public async Task<JsonDocument?> RecommendAsync(IEnumerable<string> ingredients, CancellationToken ct = default)
    {
        var response = await _http.PostAsJsonAsync("/api/v1/menu/recommender", ingredients, ct);

        if (response.StatusCode == System.Net.HttpStatusCode.UnprocessableEntity)
        {
            var error = await response.Content.ReadFromJsonAsync<HTTPValidationError>(cancellationToken: ct);
            throw new ValidationException(error);
        }

        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<JsonDocument>(cancellationToken: ct);
    }

    /// <summary>
    /// GET /api/v1/menu/menusampler – Next Menu Sampler
    /// </summary>
    public async Task<JsonDocument?> GetMenuSamplerAsync(int number, CancellationToken ct = default)
    {
        var response = await _http.GetAsync($"/api/v1/menu/menusampler?top_k={number}", ct);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<JsonDocument>(cancellationToken: ct);
    }
}

#region Error models

public sealed class HTTPValidationError
{
    public List<ValidationError>? Detail { get; set; }
}

public sealed class ValidationError
{
    public List<object>? Loc { get; set; } // string or int, OpenAPI allows both
    public string Msg { get; set; } = default!;
    public string Type { get; set; } = default!;
}

/// <summary>
/// Custom exception for validation errors
/// </summary>
public sealed class ValidationException : Exception
{
    public HTTPValidationError Error { get; }

    public ValidationException(HTTPValidationError? error)
        : base("Validation error")
    {
        Error = error ?? new HTTPValidationError();
    }
}

#endregion
