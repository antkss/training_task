// local variable allocation has failed, the output may be wrong!
__int64 __fastcall battle_field(str4 *hero, str1 *trooper, str2 *monster, unsigned int decide_value)
{
  int choice; // [rsp+2Ch] [rbp-24h] BYREF
  int userinput; // [rsp+30h] [rbp-20h] BYREF
  int control; // [rsp+34h] [rbp-1Ch]
  int i; // [rsp+38h] [rbp-18h]
  int j; // [rsp+3Ch] [rbp-14h]
  int k; // [rsp+40h] [rbp-10h]
  int random; // [rsp+44h] [rbp-Ch]
  unsigned __int64 v14; // [rsp+48h] [rbp-8h]

  v14 = __readfsqword(0x28u);
  control = 1;
  i = 0;
  j = 0;
  k = 0;
  srand(4919u);
  while ( control )
  {
    hero_index_0(hero);
    trooper_index_0(trooper);
    monster_index_0(monster);
    for ( i = 0; i <= 1 && hero[i].health <= 0; ++i )
      ;
    for ( j = 0; j <= 1 && SLODWORD(monster[j].not_health) <= 0; ++j )
      ;
    for ( k = 0; k <= 4 && trooper[k].health <= 0; ++k )
      ;
    print_string_1();                           // hero turn 
    puts("Do you wanna attack [1]monster or [0]trooper?(1/0)");
    scanf("%d", &choice);
    if ( choice == 1 )
    {
      puts("Attacking the monster....");
      random = rand() % 2022;
      printf("Guessing monster attack direction to attack\nWhat do you think? > ");
      scanf("%d", &userinput);
      if ( random == userinput )
      {
        printf("Monster is lack %d healths!\n", (hero[i].damn + hero[i].special_damn));
        LODWORD(monster[j].not_health) -= hero[i].damn + hero[i].special_damn;
      }
      else
      {
        puts("Monster blocked your attack!");
      }
      if ( SLODWORD(monster[j].not_health) < 0 )
        LODWORD(monster[j].not_health) = 0;
    }
    else if ( choice )
    {
      puts("Unknown target. Please choice 1 or 0");
    }
    else if ( k <= 4 )
    {
      puts("Kill by yourself your trooper :( ");
      trooper[k].health -= hero[i].damn;
      if ( trooper[k].health <= 0 && k <= 4 )
        hero[i].idx += 4;
    }
    else
    {
      puts("There is no trooper :(");
    }
    if ( SLODWORD(monster[j].not_health) <= 0 && j > 1 && i <= 1 )
    {
      control = 0;                              // control =0 
      hero[i].idx -= 2;
      decide_value = 1;
      put_string();
    }
    print_string_0();
    if ( k <= 4 )
    {
      puts("Attacking the monster ...");
      LODWORD(monster[j].not_health) -= trooper[k].damn;
    }
    if ( SLODWORD(monster[j].not_health) < 0 )
      LODWORD(monster[j].not_health) = 0;
    put_string_0();
    if ( i <= 1 )
    {
      puts("Attack the hero first! Kill the legion commander");
      hero[i].health -= monster[j].damn;
    }
    if ( hero[i].health < 0 && i > 1 || i > 1 ) // control = 0 
    {
      control = 0;
      put_string_1();
      decide_value = 0;
    }
  }
  return decide_value;
}
// local variable allocation has failed, the output may be wrong!
__int64 __fastcall main(
        int a1,
        char **a2,
        char **a3,
        __int64 a4,
        __int64 a5,
        __int64 a6,
        __int64 a7,
        __int64 a8,
        __int64 a9,
        __int64 decide_value)
{
  int v11; // r9d
  char *name; // rsi
  str7 *string; // rcx
  int numsof; // [rsp+8h] [rbp-188h] BYREF
  int numsofhero; // [rsp+Ch] [rbp-184h] BYREF
  unsigned int i; // [rsp+10h] [rbp-180h]
  int j; // [rsp+14h] [rbp-17Ch]
  int k; // [rsp+18h] [rbp-178h]
  int m; // [rsp+1Ch] [rbp-174h]
  char s[16]; // [rsp+20h] [rbp-170h] BYREF
  str5 hero[2]; // [rsp+30h] [rbp-160h] BYREF
  str7 str[1]; // [rsp+70h] [rbp-120h] OVERLAPPED BYREF
  str1 trooper[5]; // [rsp+C0h] [rbp-D0h] OVERLAPPED BYREF
  str2 monster[5]; // [rsp+110h] [rbp-80h] BYREF
  unsigned __int64 unknown; // [rsp+188h] [rbp-8h]

  unknown = __readfsqword(0x28u);
  setbuf(stdin, 0LL);
  setbuf(stdout, 0LL);
  setbuf(stderr, 0LL);
  memset(str, 0, 0x50uLL);
  memset(s, 0, sizeof(s));
  memset(monster, 0, sizeof(monster));
  memset(trooper, 0, sizeof(trooper));
  memset(hero, 0, sizeof(hero));
  numsof = 0;
  puts("Initiating game ...");
  puts("How many trooper(s) do you want?(0-5)");
  scanf("%d", &numsof);
  for ( i = 0; i < numsof; ++i )
  {
    snprintf(trooper[i].string, 8uLL, "Trooper%d", i);
    trooper[i].damn = 16;
    trooper[i].health = 32;
    trooper_index(*trooper[i].string, *&trooper[i].damn);
  }
  puts("How many monster do you want?(0-2)");
  scanf("%d", &numsof);
  for ( j = 0; j < numsof; ++j )
  {
    monster[j].string = &decide_value;
    monster[j].damn = 32;
    monster[j].health = 16;
    monster[j].not_health = 256;
    monster_index(
      "%d",
      &numsof,
      j,
      &decide_value,
      a1,
      v11,
      monster[j].string,
      *&monster[j].damn,
      *&monster[j].not_health);
  }
  puts("How many hero do you want?(0-2)");
  scanf("%d", &numsofhero);
  for ( k = 0; k < numsofhero; ++k )
  {
    hero[k].fame_id = k;
    hero[k].damn = 32;
    hero[k].special_damn = 48;
    hero[k].health = 512;
    puts("How do you call your hero?");
    name = hero[k].name;
    read(0, name, 16uLL);
    hero_index(
      0LL,                                      // print hero index 
      name,
      decide_value,
      decide_value,
      decide_value,
      decide_value,
      *&hero[k].fame_id,
      *&hero[k].name[4],
      *&hero[k].name[12],
      *&hero[k].special_damn);
  }
  put_string_author();
  if ( battle_field(hero, trooper, monster, &decide_value - 396) )
  {
    puts("Big won! The civilian always remember heroes!");
    puts("======== ^ HALL OF FAME ^ =========");
    for ( m = 0; m < numsofhero; ++m )
    {
      string = &str[hero[m].fame_id];
      decide_value = *&hero[m].name[8];         // long int decide_value
      *string->name = *hero[m].name;
      *&string->name[8] = decide_value;
      if ( hero[m].fame_id < 0 )
        hero[m].fame_id = 0;
      printf("Top %d - %s\n", (hero[m].fame_id + 1), hero[m].name);
    }
  }

  print_string();
  return 0LL;
}
