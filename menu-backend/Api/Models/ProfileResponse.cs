﻿namespace backend.Api.Models;

public class ProfileResponse
{
    public required string Username { get; set; }
    
    public required string Email { get; set; }
    
    public required string Household { get; set; }

    public required string HouseholdKey { get; set; }
}
