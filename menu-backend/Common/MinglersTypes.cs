namespace backend.Common;


/// <summary>
/// Generic TinyPerson
/// </summary>
public sealed record TinyPerson(
    string Type,
    PersonaDetails Persona
);

/// <summary>
/// Chef in discussion
/// </summary>
public sealed record Chef(
    string Type,
    PersonaDetails Persona
);

/// <summary>
/// Consultant in discussion
/// </summary>
public sealed record Consultant(
    string Type,
    PersonaDetails Persona
);

/// <summary>
/// Menu item under discussion
/// </summary>
public sealed record MenuItem(
    string Name,
    string Description,
    List<string>? Ingredients
);

/// <summary>
/// Rich persona details (from your JSON)
/// </summary>
public sealed record PersonaDetails(
    string Name,
    int Age,
    string Nationality,
    string? CountryOfResidence,
    Occupation Occupation,
    string Gender,
    string Residence,
    string Education,
    List<string> LongTermGoals,
    string Style,
    Personality Personality,
    Preferences Preferences,
    List<string> Beliefs,
    List<string> Skills,
    Behaviors Behaviors,
    Health Health,
    List<Relationship> Relationships,
    List<string> OtherFacts
);

public sealed record Occupation(
    string Title,
    string Organization,
    string Description
);

public sealed record Personality(
    List<string> Traits,
    BigFive BigFive
);

public sealed record BigFive(
    double Openness,
    double Conscientiousness,
    double Extraversion,
    double Agreeableness,
    double Neuroticism
);

public sealed record Preferences(
    List<string> Interests,
    List<string> Likes,
    List<string> Dislikes
);

public sealed record Behaviors(
    List<string> General,
    Routines Routines
);

public sealed record Routines(
    List<string> Morning,
    List<string> Workday,
    List<string> Evening,
    List<string> Weekend
);

public sealed record Health(
    string Physical,
    string Mental
);

public sealed record Relationship(
    string Name,
    string Description
);
