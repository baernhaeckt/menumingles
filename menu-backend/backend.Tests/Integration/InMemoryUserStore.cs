﻿using System.Collections.Concurrent;

using backend.Auth.Api;
using backend.Auth.Storage;

namespace backend.Tests.Integration;

public class InMemoryUserStore : IUserStore
{
    // Key = username
    private readonly ConcurrentDictionary<string, (User User, string Password)> _users = new();

    public Task<User?> FindByUsernameAsync(string username)
    {
        if (_users.TryGetValue(username, out var entry))
            return Task.FromResult<User?>(entry.User);

        return Task.FromResult<User?>(null);
    }

    public Task SaveAsync(User user, string password)
    {
        _users[user.Username] = (user, password);
        return Task.CompletedTask;
    }

    public Task<User?> VerifyPassword(string username, string password)
    {
        if (_users.TryGetValue(username, out var entry) && entry.Password == password)
            return Task.FromResult<User?>(entry.User);

        return Task.FromResult<User?>(null);
    }

    // For tests: seed data
    public void Seed(User user, string password)
    {
        _users[user.Username] = (user, password);
    }

    // For tests: clear
    public void Clear() => _users.Clear();
}
