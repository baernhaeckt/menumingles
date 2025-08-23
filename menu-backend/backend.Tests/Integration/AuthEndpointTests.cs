
using backend.Api.Models;

using Microsoft.AspNetCore.Mvc.Testing;

using System.Net;
using System.Net.Http.Headers;
using System.Net.Http.Json;

namespace backend.Tests.Integration;

[TestClass]
public class AuthEndpointTests
{
    private WebApplicationFactory<Program> _factory = null!;

    [TestInitialize]
    public void Setup() => _factory = new WebApplicationFactory<Program>();

    [TestCleanup]
    public void Cleanup() => _factory?.Dispose();

    [TestMethod]
    public async Task AuthRegisterEndpoint_ShouldReturn200Ok()
    {
        // Arrange
        var client = _factory.CreateClient();

        // Act
        var response = await client.PostAsJsonAsync("/api/v1/auth/register", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123"
        });

        // Assert
        Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
    }

    [TestMethod]
    public async Task AuthLoginEndpoint_ShouldReturn200OkAndToken()
    {
        // Arrange
        var client = _factory.CreateClient();

        // Act
        var response = await client.PostAsJsonAsync("/api/v1/auth/login", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123"
        });

        // Assert
        string token = await response.Content.ReadAsStringAsync();
        Assert.AreEqual(HttpStatusCode.OK, response.StatusCode);
    }

    [TestMethod]
    public async Task AuthMeEndpoint_ShouldReturn200OkAndUser()
    {
        // Arrange
        var client = _factory.CreateClient();

        // Act
        var response = await client.PostAsJsonAsync("/api/v1/auth/login", new RegisterRequest()
        {
            Username = "testuser",
            Email = "tester@test.ch",
            Password = "Test123"
        });
        string token = await response.Content.ReadAsStringAsync();
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        var meResponse = await client.GetAsync("/api/v1/auth/me");

        // Assert
        Assert.AreEqual(HttpStatusCode.OK, meResponse.StatusCode);
        string meContent = await meResponse.Content.ReadAsStringAsync();
    }
}
