/******************************
  Program "past_builds/VI_buggy_build/s4_constrained/out/P_V_ci_evict_0_1_sent.m" compiled by "Caching Murphi Release 5.4.9.1"

  Murphi Last Compiled date: "Jan 31 2025"
 ******************************/

/********************
  Parameter
 ********************/
#define MURPHI_VERSION "Caching Murphi Release 5.4.9.1"
#define MURPHI_DATE "Jan 31 2025"
#define PROTOCOL_NAME "past_builds/VI_buggy_build/s4_constrained/out/P_V_ci_evict_0_1_sent"
#define BITS_IN_WORLD 472
#define ALIGN

/********************
  Include
 ********************/
#include "mu_prolog.hpp"

/********************
  Decl declaration
 ********************/

class mu_1_Proc: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_Proc& val){ return value(val.value());};
  inline operator int() const { return value(); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_Proc& val)
    {
      if (val.defined())
	return ( s << mu_1_Proc::values[ int(val) - 1 ] );
      else
	return ( s << "Undefined" );
    };

  mu_1_Proc (const char *name, int os): mu__byte(1, 3, 2, name, os) {};
  mu_1_Proc (void): mu__byte(1, 3, 2) {};
  mu_1_Proc (int val): mu__byte(1, 3, 2, "Parameter or function result.", 0)
    { operator=(val); };
  const char * Name() { return values[ value() -1]; };
  virtual void print()
    {
      if (defined()) cout << name << ':' << values[ value() - 1] << '\n';
      else cout << name << ":Undefined\n";
    };
  void print_statistic() {};
friend int CompareWeight(mu_1_Proc& a, mu_1_Proc& b)
{
  if (!a.defined() && b.defined())
    return -1;
  else if (a.defined() && !b.defined())
    return 1;
  else
    return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
};
const char *mu_1_Proc::values[] =
  { "Proc_1","Proc_2","Proc_3",NULL };

/*** end scalarset declaration ***/
mu_1_Proc mu_1_Proc_undefined_var;

class mu_1_Value: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_Value& val){ return value(val.value());};
  inline operator int() const { return value(); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_Value& val)
    {
      if (val.defined())
	return ( s << mu_1_Value::values[ int(val) - 4 ] );
      else
	return ( s << "Undefined" );
    };

  mu_1_Value (const char *name, int os): mu__byte(4, 5, 2, name, os) {};
  mu_1_Value (void): mu__byte(4, 5, 2) {};
  mu_1_Value (int val): mu__byte(4, 5, 2, "Parameter or function result.", 0)
    { operator=(val); };
  const char * Name() { return values[ value() -4]; };
  virtual void print()
    {
      if (defined()) cout << name << ':' << values[ value() - 4] << '\n';
      else cout << name << ":Undefined\n";
    };
  void print_statistic() {};
friend int CompareWeight(mu_1_Value& a, mu_1_Value& b)
{
  if (!a.defined() && b.defined())
    return -1;
  else if (a.defined() && !b.defined())
    return 1;
  else
    return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
};
const char *mu_1_Value::values[] =
  { "Value_1","Value_2",NULL };

/*** end scalarset declaration ***/
mu_1_Value mu_1_Value_undefined_var;

class mu_1_Home: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_Home& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_Home& val)
  {
    if (val.defined())
      return ( s << mu_1_Home::values[ int(val) - 6] );
    else return ( s << "Undefined" );
  };

  mu_1_Home (const char *name, int os): mu__byte(6, 6, 1, name, os) {};
  mu_1_Home (void): mu__byte(6, 6, 1) {};
  mu_1_Home (int val): mu__byte(6, 6, 1, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -6]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -6] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1_Home::values[] = {"HomeType",NULL };

/*** end of enum declaration ***/
mu_1_Home mu_1_Home_undefined_var;

class mu_1_Node: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_Node& val) { return value(val.value()); };
  inline operator int() const { return value(); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_Node& val)
    {
      if (val.defined())
	return ( s << mu_1_Node::values[ val.indexvalue() ] );
      else
	return ( s << "Undefined" );
    };

  // note thate lb and ub are not used if we have byte compacted state.
  mu_1_Node (const char *name, int os): mu__byte(0, 3, 3, name, os) {};
  mu_1_Node (void): mu__byte(0, 3, 3) {};
  mu_1_Node (int val): mu__byte(0, 3, 3, "Parameter or function result.", 0)
    { operator=(val); };
  int indexvalue()
  {
    if ((value() >= 6) && (value() <= 6)) return (value() - 6);
    if ((value() >= 1) && (value() <= 3)) return (value() - 0);
  return 0;
  };
  inline int unionassign(int val)
  {
    if (val >= 0 && val <= 0) return value(val+6);
    if (val >= 1 && val <= 3) return value(val+0);
  return 0;
  };
  const char * Name() { return values[ indexvalue() ]; };
friend int CompareWeight(mu_1_Node& a, mu_1_Node& b)
{
  if (!a.defined() && b.defined())
    return -1;
  else if (a.defined() && !b.defined())
    return 1;
  else
    return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void print()
    {
      if (defined()) cout << name << ':' << values[ indexvalue() ] << '\n';
      else cout << name << ":Undefined\n";
    };
  void print_statistic() {};
};
const char *mu_1_Node::values[] = {"HomeType","Proc_1","Proc_2","Proc_3",NULL };

/*** end union declaration ***/
mu_1_Node mu_1_Node_undefined_var;

class mu_1__type_0: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1__type_0& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1__type_0& val)
  {
    if (val.defined())
      return ( s << mu_1__type_0::values[ int(val) - 7] );
    else return ( s << "Undefined" );
  };

  mu_1__type_0 (const char *name, int os): mu__byte(7, 9, 2, name, os) {};
  mu_1__type_0 (void): mu__byte(7, 9, 2) {};
  mu_1__type_0 (int val): mu__byte(7, 9, 2, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -7]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -7] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1__type_0::values[] = {"store","load","evict",NULL };

/*** end of enum declaration ***/
mu_1__type_0 mu_1__type_0_undefined_var;

class mu_1_CurReq
{
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  void set_self(const char *n, int os);
  mu_1_Value mu_val;
  mu_1__type_0 mu_tp;
  mu_0_boolean mu_vld;
  mu_1_CurReq ( const char *n, int os ) { set_self(n,os); };
  mu_1_CurReq ( void ) {};

  virtual ~mu_1_CurReq(); 
friend int CompareWeight(mu_1_CurReq& a, mu_1_CurReq& b)
  {
    int w;
    w = CompareWeight(a.mu_val, b.mu_val);
    if (w!=0) return w;
    w = CompareWeight(a.mu_tp, b.mu_tp);
    if (w!=0) return w;
    w = CompareWeight(a.mu_vld, b.mu_vld);
    if (w!=0) return w;
  return 0;
}
friend int Compare(mu_1_CurReq& a, mu_1_CurReq& b)
  {
    int w;
    w = Compare(a.mu_val, b.mu_val);
    if (w!=0) return w;
    w = Compare(a.mu_tp, b.mu_tp);
    if (w!=0) return w;
    w = Compare(a.mu_vld, b.mu_vld);
    if (w!=0) return w;
  return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    mu_val.MultisetSort();
    mu_tp.MultisetSort();
    mu_vld.MultisetSort();
  }
  void print_statistic()
  {
    mu_val.print_statistic();
    mu_tp.print_statistic();
    mu_vld.print_statistic();
  }
  void clear() {
    mu_val.clear();
    mu_tp.clear();
    mu_vld.clear();
 };
  void undefine() {
    mu_val.undefine();
    mu_tp.undefine();
    mu_vld.undefine();
 };
  void reset() {
    mu_val.reset();
    mu_tp.reset();
    mu_vld.reset();
 };
  void print() {
    mu_val.print();
    mu_tp.print();
    mu_vld.print();
  };
  void print_diff(state *prevstate) {
    mu_val.print_diff(prevstate);
    mu_tp.print_diff(prevstate);
    mu_vld.print_diff(prevstate);
  };
  void to_state(state *thestate) {
    mu_val.to_state(thestate);
    mu_tp.to_state(thestate);
    mu_vld.to_state(thestate);
  };
virtual bool isundefined() { Error.Error("Checking undefinedness of a non-base type"); return TRUE;}
virtual bool ismember() { Error.Error("Checking membership for a non-base type"); return TRUE;}
  mu_1_CurReq& operator= (const mu_1_CurReq& from) {
    mu_val.value(from.mu_val.value());
    mu_tp.value(from.mu_tp.value());
    mu_vld.value(from.mu_vld.value());
    return *this;
  };
};

  void mu_1_CurReq::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1_CurReq::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1_CurReq::set_self(const char *n, int os)
{
  name = (char *)n;

  if (name) mu_val.set_self_2(name, ".val", os + 0 ); else mu_val.set_self_2(NULL, NULL, 0);
  if (name) mu_tp.set_self_2(name, ".tp", os + 8 ); else mu_tp.set_self_2(NULL, NULL, 0);
  if (name) mu_vld.set_self_2(name, ".vld", os + 16 ); else mu_vld.set_self_2(NULL, NULL, 0);
}

mu_1_CurReq::~mu_1_CurReq()
{
}

/*** end record declaration ***/
mu_1_CurReq mu_1_CurReq_undefined_var;

class mu_1_MessageType: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_MessageType& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_MessageType& val)
  {
    if (val.defined())
      return ( s << mu_1_MessageType::values[ int(val) - 10] );
    else return ( s << "Undefined" );
  };

  mu_1_MessageType (const char *name, int os): mu__byte(10, 12, 2, name, os) {};
  mu_1_MessageType (void): mu__byte(10, 12, 2) {};
  mu_1_MessageType (int val): mu__byte(10, 12, 2, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -10]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -10] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1_MessageType::values[] = {"GetMsg","PutMsg","DataRespMsg",NULL };

/*** end of enum declaration ***/
mu_1_MessageType mu_1_MessageType_undefined_var;

class mu_1_Message
{
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  void set_self(const char *n, int os);
  mu_1_MessageType mu_mtype;
  mu_1_Node mu_src;
  mu_1_Node mu_dst;
  mu_1_Value mu_val;
  mu_1_Message ( const char *n, int os ) { set_self(n,os); };
  mu_1_Message ( void ) {};

  virtual ~mu_1_Message(); 
friend int CompareWeight(mu_1_Message& a, mu_1_Message& b)
  {
    int w;
    w = CompareWeight(a.mu_mtype, b.mu_mtype);
    if (w!=0) return w;
    w = CompareWeight(a.mu_src, b.mu_src);
    if (w!=0) return w;
    w = CompareWeight(a.mu_dst, b.mu_dst);
    if (w!=0) return w;
    w = CompareWeight(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
friend int Compare(mu_1_Message& a, mu_1_Message& b)
  {
    int w;
    w = Compare(a.mu_mtype, b.mu_mtype);
    if (w!=0) return w;
    w = Compare(a.mu_src, b.mu_src);
    if (w!=0) return w;
    w = Compare(a.mu_dst, b.mu_dst);
    if (w!=0) return w;
    w = Compare(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    mu_mtype.MultisetSort();
    mu_src.MultisetSort();
    mu_dst.MultisetSort();
    mu_val.MultisetSort();
  }
  void print_statistic()
  {
    mu_mtype.print_statistic();
    mu_src.print_statistic();
    mu_dst.print_statistic();
    mu_val.print_statistic();
  }
  void clear() {
    mu_mtype.clear();
    mu_src.clear();
    mu_dst.clear();
    mu_val.clear();
 };
  void undefine() {
    mu_mtype.undefine();
    mu_src.undefine();
    mu_dst.undefine();
    mu_val.undefine();
 };
  void reset() {
    mu_mtype.reset();
    mu_src.reset();
    mu_dst.reset();
    mu_val.reset();
 };
  void print() {
    mu_mtype.print();
    mu_src.print();
    mu_dst.print();
    mu_val.print();
  };
  void print_diff(state *prevstate) {
    mu_mtype.print_diff(prevstate);
    mu_src.print_diff(prevstate);
    mu_dst.print_diff(prevstate);
    mu_val.print_diff(prevstate);
  };
  void to_state(state *thestate) {
    mu_mtype.to_state(thestate);
    mu_src.to_state(thestate);
    mu_dst.to_state(thestate);
    mu_val.to_state(thestate);
  };
virtual bool isundefined() { Error.Error("Checking undefinedness of a non-base type"); return TRUE;}
virtual bool ismember() { Error.Error("Checking membership for a non-base type"); return TRUE;}
  mu_1_Message& operator= (const mu_1_Message& from) {
    mu_mtype.value(from.mu_mtype.value());
    mu_src.value(from.mu_src.value());
    mu_dst.value(from.mu_dst.value());
    mu_val.value(from.mu_val.value());
    return *this;
  };
};

  void mu_1_Message::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1_Message::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1_Message::set_self(const char *n, int os)
{
  name = (char *)n;

  if (name) mu_mtype.set_self_2(name, ".mtype", os + 0 ); else mu_mtype.set_self_2(NULL, NULL, 0);
  if (name) mu_src.set_self_2(name, ".src", os + 8 ); else mu_src.set_self_2(NULL, NULL, 0);
  if (name) mu_dst.set_self_2(name, ".dst", os + 16 ); else mu_dst.set_self_2(NULL, NULL, 0);
  if (name) mu_val.set_self_2(name, ".val", os + 24 ); else mu_val.set_self_2(NULL, NULL, 0);
}

mu_1_Message::~mu_1_Message()
{
}

/*** end record declaration ***/
mu_1_Message mu_1_Message_undefined_var;

class mu_1_HomeStateEnum: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_HomeStateEnum& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_HomeStateEnum& val)
  {
    if (val.defined())
      return ( s << mu_1_HomeStateEnum::values[ int(val) - 13] );
    else return ( s << "Undefined" );
  };

  mu_1_HomeStateEnum (const char *name, int os): mu__byte(13, 14, 2, name, os) {};
  mu_1_HomeStateEnum (void): mu__byte(13, 14, 2) {};
  mu_1_HomeStateEnum (int val): mu__byte(13, 14, 2, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -13]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -13] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1_HomeStateEnum::values[] = {"H_I","H_V",NULL };

/*** end of enum declaration ***/
mu_1_HomeStateEnum mu_1_HomeStateEnum_undefined_var;

class mu_1_HomeState
{
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  void set_self(const char *n, int os);
  mu_1_HomeStateEnum mu_state;
  mu_1_Value mu_val;
  mu_1_HomeState ( const char *n, int os ) { set_self(n,os); };
  mu_1_HomeState ( void ) {};

  virtual ~mu_1_HomeState(); 
friend int CompareWeight(mu_1_HomeState& a, mu_1_HomeState& b)
  {
    int w;
    w = CompareWeight(a.mu_state, b.mu_state);
    if (w!=0) return w;
    w = CompareWeight(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
friend int Compare(mu_1_HomeState& a, mu_1_HomeState& b)
  {
    int w;
    w = Compare(a.mu_state, b.mu_state);
    if (w!=0) return w;
    w = Compare(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    mu_state.MultisetSort();
    mu_val.MultisetSort();
  }
  void print_statistic()
  {
    mu_state.print_statistic();
    mu_val.print_statistic();
  }
  void clear() {
    mu_state.clear();
    mu_val.clear();
 };
  void undefine() {
    mu_state.undefine();
    mu_val.undefine();
 };
  void reset() {
    mu_state.reset();
    mu_val.reset();
 };
  void print() {
    mu_state.print();
    mu_val.print();
  };
  void print_diff(state *prevstate) {
    mu_state.print_diff(prevstate);
    mu_val.print_diff(prevstate);
  };
  void to_state(state *thestate) {
    mu_state.to_state(thestate);
    mu_val.to_state(thestate);
  };
virtual bool isundefined() { Error.Error("Checking undefinedness of a non-base type"); return TRUE;}
virtual bool ismember() { Error.Error("Checking membership for a non-base type"); return TRUE;}
  mu_1_HomeState& operator= (const mu_1_HomeState& from) {
    mu_state.value(from.mu_state.value());
    mu_val.value(from.mu_val.value());
    return *this;
  };
};

  void mu_1_HomeState::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1_HomeState::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1_HomeState::set_self(const char *n, int os)
{
  name = (char *)n;

  if (name) mu_state.set_self_2(name, ".state", os + 0 ); else mu_state.set_self_2(NULL, NULL, 0);
  if (name) mu_val.set_self_2(name, ".val", os + 8 ); else mu_val.set_self_2(NULL, NULL, 0);
}

mu_1_HomeState::~mu_1_HomeState()
{
}

/*** end record declaration ***/
mu_1_HomeState mu_1_HomeState_undefined_var;

class mu_1_ProcStateEnum: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1_ProcStateEnum& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1_ProcStateEnum& val)
  {
    if (val.defined())
      return ( s << mu_1_ProcStateEnum::values[ int(val) - 15] );
    else return ( s << "Undefined" );
  };

  mu_1_ProcStateEnum (const char *name, int os): mu__byte(15, 17, 2, name, os) {};
  mu_1_ProcStateEnum (void): mu__byte(15, 17, 2) {};
  mu_1_ProcStateEnum (int val): mu__byte(15, 17, 2, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -15]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -15] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1_ProcStateEnum::values[] = {"P_I","P_IVD","P_V",NULL };

/*** end of enum declaration ***/
mu_1_ProcStateEnum mu_1_ProcStateEnum_undefined_var;

class mu_1_ProcState
{
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  void set_self(const char *n, int os);
  mu_1_ProcStateEnum mu_state;
  mu_1_Value mu_val;
  mu_1_ProcState ( const char *n, int os ) { set_self(n,os); };
  mu_1_ProcState ( void ) {};

  virtual ~mu_1_ProcState(); 
friend int CompareWeight(mu_1_ProcState& a, mu_1_ProcState& b)
  {
    int w;
    w = CompareWeight(a.mu_state, b.mu_state);
    if (w!=0) return w;
    w = CompareWeight(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
friend int Compare(mu_1_ProcState& a, mu_1_ProcState& b)
  {
    int w;
    w = Compare(a.mu_state, b.mu_state);
    if (w!=0) return w;
    w = Compare(a.mu_val, b.mu_val);
    if (w!=0) return w;
  return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    mu_state.MultisetSort();
    mu_val.MultisetSort();
  }
  void print_statistic()
  {
    mu_state.print_statistic();
    mu_val.print_statistic();
  }
  void clear() {
    mu_state.clear();
    mu_val.clear();
 };
  void undefine() {
    mu_state.undefine();
    mu_val.undefine();
 };
  void reset() {
    mu_state.reset();
    mu_val.reset();
 };
  void print() {
    mu_state.print();
    mu_val.print();
  };
  void print_diff(state *prevstate) {
    mu_state.print_diff(prevstate);
    mu_val.print_diff(prevstate);
  };
  void to_state(state *thestate) {
    mu_state.to_state(thestate);
    mu_val.to_state(thestate);
  };
virtual bool isundefined() { Error.Error("Checking undefinedness of a non-base type"); return TRUE;}
virtual bool ismember() { Error.Error("Checking membership for a non-base type"); return TRUE;}
  mu_1_ProcState& operator= (const mu_1_ProcState& from) {
    mu_state.value(from.mu_state.value());
    mu_val.value(from.mu_val.value());
    return *this;
  };
};

  void mu_1_ProcState::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1_ProcState::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1_ProcState::set_self(const char *n, int os)
{
  name = (char *)n;

  if (name) mu_state.set_self_2(name, ".state", os + 0 ); else mu_state.set_self_2(NULL, NULL, 0);
  if (name) mu_val.set_self_2(name, ".val", os + 8 ); else mu_val.set_self_2(NULL, NULL, 0);
}

mu_1_ProcState::~mu_1_ProcState()
{
}

/*** end record declaration ***/
mu_1_ProcState mu_1_ProcState_undefined_var;

class mu_1__type_1: public mu__byte
{
 public:
  inline int operator=(int val) { return value(val); };
  inline int operator=(const mu_1__type_1& val) { return value(val.value()); };
  static const char *values[];
  friend ostream& operator<< (ostream& s, mu_1__type_1& val)
  {
    if (val.defined())
      return ( s << mu_1__type_1::values[ int(val) - 18] );
    else return ( s << "Undefined" );
  };

  mu_1__type_1 (const char *name, int os): mu__byte(18, 20, 2, name, os) {};
  mu_1__type_1 (void): mu__byte(18, 20, 2) {};
  mu_1__type_1 (int val): mu__byte(18, 20, 2, "Parameter or function result.", 0)
  {
     operator=(val);
  };
  const char * Name() { return values[ value() -18]; };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
  virtual void print()
  {
    if (defined())
      cout << name << ":" << values[ value() -18] << '\n';
    else
      cout << name << ":Undefined\n";
  };
};

const char *mu_1__type_1::values[] = {"ci_store","ci_load","ci_evict",NULL };

/*** end of enum declaration ***/
mu_1__type_1 mu_1__type_1_undefined_var;

class mu_1_CoreReq
{
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  void set_self(const char *n, int os);
  mu_1_Value mu_cl;
  mu_0_boolean mu_vld;
  mu_1__type_1 mu_tp;
  mu_1_CoreReq ( const char *n, int os ) { set_self(n,os); };
  mu_1_CoreReq ( void ) {};

  virtual ~mu_1_CoreReq(); 
friend int CompareWeight(mu_1_CoreReq& a, mu_1_CoreReq& b)
  {
    int w;
    w = CompareWeight(a.mu_cl, b.mu_cl);
    if (w!=0) return w;
    w = CompareWeight(a.mu_vld, b.mu_vld);
    if (w!=0) return w;
    w = CompareWeight(a.mu_tp, b.mu_tp);
    if (w!=0) return w;
  return 0;
}
friend int Compare(mu_1_CoreReq& a, mu_1_CoreReq& b)
  {
    int w;
    w = Compare(a.mu_cl, b.mu_cl);
    if (w!=0) return w;
    w = Compare(a.mu_vld, b.mu_vld);
    if (w!=0) return w;
    w = Compare(a.mu_tp, b.mu_tp);
    if (w!=0) return w;
  return 0;
}
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    mu_cl.MultisetSort();
    mu_vld.MultisetSort();
    mu_tp.MultisetSort();
  }
  void print_statistic()
  {
    mu_cl.print_statistic();
    mu_vld.print_statistic();
    mu_tp.print_statistic();
  }
  void clear() {
    mu_cl.clear();
    mu_vld.clear();
    mu_tp.clear();
 };
  void undefine() {
    mu_cl.undefine();
    mu_vld.undefine();
    mu_tp.undefine();
 };
  void reset() {
    mu_cl.reset();
    mu_vld.reset();
    mu_tp.reset();
 };
  void print() {
    mu_cl.print();
    mu_vld.print();
    mu_tp.print();
  };
  void print_diff(state *prevstate) {
    mu_cl.print_diff(prevstate);
    mu_vld.print_diff(prevstate);
    mu_tp.print_diff(prevstate);
  };
  void to_state(state *thestate) {
    mu_cl.to_state(thestate);
    mu_vld.to_state(thestate);
    mu_tp.to_state(thestate);
  };
virtual bool isundefined() { Error.Error("Checking undefinedness of a non-base type"); return TRUE;}
virtual bool ismember() { Error.Error("Checking membership for a non-base type"); return TRUE;}
  mu_1_CoreReq& operator= (const mu_1_CoreReq& from) {
    mu_cl.value(from.mu_cl.value());
    mu_vld.value(from.mu_vld.value());
    mu_tp.value(from.mu_tp.value());
    return *this;
  };
};

  void mu_1_CoreReq::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1_CoreReq::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1_CoreReq::set_self(const char *n, int os)
{
  name = (char *)n;

  if (name) mu_cl.set_self_2(name, ".cl", os + 0 ); else mu_cl.set_self_2(NULL, NULL, 0);
  if (name) mu_vld.set_self_2(name, ".vld", os + 8 ); else mu_vld.set_self_2(NULL, NULL, 0);
  if (name) mu_tp.set_self_2(name, ".tp", os + 16 ); else mu_tp.set_self_2(NULL, NULL, 0);
}

mu_1_CoreReq::~mu_1_CoreReq()
{
}

/*** end record declaration ***/
mu_1_CoreReq mu_1_CoreReq_undefined_var;

class mu_1__type_2
{
 public:
  mu_0_boolean array[ 3 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_2 (const char *n, int os) { set_self(n, os); };
  mu_1__type_2 ( void ) {};
  virtual ~mu_1__type_2 ();
  mu_0_boolean& operator[] (int index) /* const */
  {
#ifndef NO_RUN_TIME_CHECKING
    if ( ( index >= 10 ) && ( index <= 12 ) )
      return array[ index - 10 ];
    else {
      if (index==UNDEFVAL) 
	Error.Error("Indexing to %s using an undefined value.", name);
      else
	Error.Error("%d not in index range of %s.", index, name);
      return array[0];
    }
#else
    return array[ index - 10 ];
#endif
  };
  mu_1__type_2& operator= (const mu_1__type_2& from)
  {
    for (int i = 0; i < 3; i++)
      array[i].value(from.array[i].value());
    return *this;
  }

friend int CompareWeight(mu_1__type_2& a, mu_1__type_2& b)
  {
    int w;
    for (int i=0; i<3; i++) {
      w = CompareWeight(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
friend int Compare(mu_1__type_2& a, mu_1__type_2& b)
  {
    int w;
    for (int i=0; i<3; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<3; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<3; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 3; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 3; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 3; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 3; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 3; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 3; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_2::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_2::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
  void mu_1__type_2::set_self( const char *n, int os)
  {
    int i=0;
    name = (char *)n;

if (n) array[i].set_self_ar(n,"GetMsg", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"PutMsg", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"DataRespMsg", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
  }
mu_1__type_2::~mu_1__type_2()
{
}
/*** end array declaration ***/
mu_1__type_2 mu_1__type_2_undefined_var;

class mu_1__type_3: public mu__byte
{
 public:
  inline int operator=(int val) { return mu__byte::operator=(val); };
  inline int operator=(const mu_1__type_3& val) { return mu__byte::operator=((int) val); };
  mu_1__type_3 (const char *name, int os): mu__byte(0, 2, 2, name, os) {};
  mu_1__type_3 (void): mu__byte(0, 2, 2) {};
  mu_1__type_3 (int val): mu__byte(0, 2, 2, "Parameter or function result.", 0)
  {
    operator=(val);
  };
  char * Name() { return tsprintf("%d",value()); };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
};

/*** end of subrange decl ***/
mu_1__type_3 mu_1__type_3_undefined_var;

class mu__subrange_19: public mu__byte
{
 public:
  inline int operator=(int val) { return mu__byte::operator=(val); };
  inline int operator=(const mu__subrange_19& val) { return mu__byte::operator=((int) val); };
  mu__subrange_19 (const char *name, int os): mu__byte(0, 0, 1, name, os) {};
  mu__subrange_19 (void): mu__byte(0, 0, 1) {};
  mu__subrange_19 (int val): mu__byte(0, 0, 1, "Parameter or function result.", 0)
  {
    operator=(val);
  };
  char * Name() { return tsprintf("%d",value()); };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
};

/*** end of subrange decl ***/
mu__subrange_19 mu__subrange_19_undefined_var;

class mu_1__type_4
{
 public:
  mu_1_ProcStateEnum array[ 1 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_4 (const char *n, int os) { set_self(n, os); };
  mu_1__type_4 ( void ) {};
  virtual ~mu_1__type_4 ();
  mu_1_ProcStateEnum& operator[] (int index) /* const */
  {
#ifndef NO_RUN_TIME_CHECKING
    if ( ( index >= 0 ) && ( index <= 0 ) )
      return array[ index - 0 ];
    else {
      if (index==UNDEFVAL) 
	Error.Error("Indexing to %s using an undefined value.", name);
      else
	Error.Error("%d not in index range of %s.", index, name);
      return array[0];
    }
#else
    return array[ index - 0 ];
#endif
  };
  mu_1__type_4& operator= (const mu_1__type_4& from)
  {
      array[0].value(from.array[0].value());
    return *this;
  }

friend int CompareWeight(mu_1__type_4& a, mu_1__type_4& b)
  {
    int w;
    for (int i=0; i<1; i++) {
      w = CompareWeight(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
friend int Compare(mu_1__type_4& a, mu_1__type_4& b)
  {
    int w;
    for (int i=0; i<1; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<1; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<1; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 1; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 1; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 1; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 1; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 1; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 1; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_4::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_4::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1__type_4::set_self( const char *n, int os)
{
  char* s;
  name = (char *)n;
  for(int i = 0; i < 1; i++) {
    array[i].set_self_ar(n, s=tsprintf("%d",i + 0), i * 8 + os);
    delete[] s;
  }
};
mu_1__type_4::~mu_1__type_4()
{
}
/*** end array declaration ***/
mu_1__type_4 mu_1__type_4_undefined_var;

class mu_1__type_5: public mu__byte
{
 public:
  inline int operator=(int val) { return mu__byte::operator=(val); };
  inline int operator=(const mu_1__type_5& val) { return mu__byte::operator=((int) val); };
  mu_1__type_5 (const char *name, int os): mu__byte(0, 2, 2, name, os) {};
  mu_1__type_5 (void): mu__byte(0, 2, 2) {};
  mu_1__type_5 (int val): mu__byte(0, 2, 2, "Parameter or function result.", 0)
  {
    operator=(val);
  };
  char * Name() { return tsprintf("%d",value()); };
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort() {};
  void print_statistic() {};
};

/*** end of subrange decl ***/
mu_1__type_5 mu_1__type_5_undefined_var;

class mu_1__type_6
{
 public:
  mu_1_ProcState array[ 3 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_6 (const char *n, int os) { set_self(n, os); };
  mu_1__type_6 ( void ) {};
  virtual ~mu_1__type_6 ();
  mu_1_ProcState& operator[] (int index) /* const */
  {
#ifndef NO_RUN_TIME_CHECKING
    if ( ( index >= 1 ) && ( index <= 3 ) )
      return array[ index - 1 ];
    else
      {
	if (index==UNDEFVAL) 
	  Error.Error("Indexing to %s using an undefined value.", name);
	else
	  Error.Error("Funny index value %d for %s: Proc is internally represented from 1 to 3.\nInternal Error in Type checking.",index, name);
	return array[0];
      }
#else
    return array[ index - 1 ];
#endif
  };
  mu_1__type_6& operator= (const mu_1__type_6& from)
  {
    for (int i = 0; i < 3; i++)
      array[i] = from.array[i];
    return *this;
  }

friend int CompareWeight(mu_1__type_6& a, mu_1__type_6& b)
  {
    return 0;
  }
friend int Compare(mu_1__type_6& a, mu_1__type_6& b)
  {
    int w;
    for (int i=0; i<3; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<3; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<3; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 3; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 3; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 3; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 3; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 3; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 3; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_6::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_6::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1__type_6::set_self( const char *n, int os)
  {
    int i=0;
    name = (char *)n;

if (n) array[i].set_self_ar(n,"Proc_1", i * 16 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_2", i * 16 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_3", i * 16 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
}
mu_1__type_6::~mu_1__type_6()
{
}
/*** end array declaration ***/
mu_1__type_6 mu_1__type_6_undefined_var;

class mu_1__type_7
{
 public:
  mu_0_boolean array[ 4 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_7 (const char *n, int os) { set_self(n, os); };
  mu_1__type_7 ( void ) {};
  virtual ~mu_1__type_7 ();
  mu_0_boolean& operator[] (int index) /* const */
  {
    if ( ( index >= 6 ) && ( index <= 6 ) )
      return array[ index - (6) ];
    if ( ( index >= 1 ) && ( index <= 3 ) )
      return array[ index - (0) ];
    if (index==UNDEFVAL) 
      Error.Error("Indexing to %s using an undefined value.", name);
    else
      Error.Error("Funny index value %d for %s. (Internal Error in Type Checking.",index, name);
    return array[0];
  }
  mu_1__type_7& operator= (const mu_1__type_7& from)
  {
    for (int i = 0; i < 4; i++)
      array[i].value(from.array[i].value());
    return *this;
  }

friend int CompareWeight(mu_1__type_7& a, mu_1__type_7& b)
  {
    return 0;
  }
friend int Compare(mu_1__type_7& a, mu_1__type_7& b)
  {
    int w;
    for (int i=0; i<4; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<4; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<4; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 4; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 4; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 4; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 4; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 4; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 4; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_7::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_7::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1__type_7::set_self( const char *n, int os)
  {
    int i=0;
    name = (char *)n;

if (n) array[i].set_self_ar(n,"HomeType", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_1", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_2", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_3", i * 8 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
}
mu_1__type_7::~mu_1__type_7()
{
}
/*** end array declaration ***/
mu_1__type_7 mu_1__type_7_undefined_var;

class mu_1__type_8
{
 public:
  mu_1_Message array[ 4 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_8 (const char *n, int os) { set_self(n, os); };
  mu_1__type_8 ( void ) {};
  virtual ~mu_1__type_8 ();
  mu_1_Message& operator[] (int index) /* const */
  {
    if ( ( index >= 6 ) && ( index <= 6 ) )
      return array[ index - (6) ];
    if ( ( index >= 1 ) && ( index <= 3 ) )
      return array[ index - (0) ];
    if (index==UNDEFVAL) 
      Error.Error("Indexing to %s using an undefined value.", name);
    else
      Error.Error("Funny index value %d for %s. (Internal Error in Type Checking.",index, name);
    return array[0];
  }
  mu_1__type_8& operator= (const mu_1__type_8& from)
  {
    for (int i = 0; i < 4; i++)
      array[i] = from.array[i];
    return *this;
  }

friend int CompareWeight(mu_1__type_8& a, mu_1__type_8& b)
  {
    return 0;
  }
friend int Compare(mu_1__type_8& a, mu_1__type_8& b)
  {
    int w;
    for (int i=0; i<4; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<4; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<4; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 4; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 4; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 4; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 4; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 4; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 4; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_8::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_8::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1__type_8::set_self( const char *n, int os)
  {
    int i=0;
    name = (char *)n;

if (n) array[i].set_self_ar(n,"HomeType", i * 32 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_1", i * 32 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_2", i * 32 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_3", i * 32 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
}
mu_1__type_8::~mu_1__type_8()
{
}
/*** end array declaration ***/
mu_1__type_8 mu_1__type_8_undefined_var;

class mu_1__type_9
{
 public:
  mu_1_CurReq array[ 3 ];
 public:
  char *name;
  char longname[BUFFER_SIZE/4];
  void set_self( const char *n, int os);
  void set_self_2( const char *n, const char *n2, int os);
  void set_self_ar( const char *n, const char *n2, int os);
  mu_1__type_9 (const char *n, int os) { set_self(n, os); };
  mu_1__type_9 ( void ) {};
  virtual ~mu_1__type_9 ();
  mu_1_CurReq& operator[] (int index) /* const */
  {
#ifndef NO_RUN_TIME_CHECKING
    if ( ( index >= 1 ) && ( index <= 3 ) )
      return array[ index - 1 ];
    else
      {
	if (index==UNDEFVAL) 
	  Error.Error("Indexing to %s using an undefined value.", name);
	else
	  Error.Error("Funny index value %d for %s: Proc is internally represented from 1 to 3.\nInternal Error in Type checking.",index, name);
	return array[0];
      }
#else
    return array[ index - 1 ];
#endif
  };
  mu_1__type_9& operator= (const mu_1__type_9& from)
  {
    for (int i = 0; i < 3; i++)
      array[i] = from.array[i];
    return *this;
  }

friend int CompareWeight(mu_1__type_9& a, mu_1__type_9& b)
  {
    return 0;
  }
friend int Compare(mu_1__type_9& a, mu_1__type_9& b)
  {
    int w;
    for (int i=0; i<3; i++) {
      w = Compare(a.array[i], b.array[i]);
      if (w!=0) return w;
    }
    return 0;
  }
  virtual void Permute(PermSet& Perm, int i);
  virtual void SimpleCanonicalize(PermSet& Perm);
  virtual void Canonicalize(PermSet& Perm);
  virtual void SimpleLimit(PermSet& Perm);
  virtual void ArrayLimit(PermSet& Perm);
  virtual void Limit(PermSet& Perm);
  virtual void MultisetLimit(PermSet& Perm);
  virtual void MultisetSort()
  {
    for (int i=0; i<3; i++)
      array[i].MultisetSort();
  }
  void print_statistic()
  {
    for (int i=0; i<3; i++)
      array[i].print_statistic();
  }
  void clear() { for (int i = 0; i < 3; i++) array[i].clear(); };

  void undefine() { for (int i = 0; i < 3; i++) array[i].undefine(); };

  void reset() { for (int i = 0; i < 3; i++) array[i].reset(); };

  void to_state(state *thestate)
  {
    for (int i = 0; i < 3; i++)
      array[i].to_state(thestate);
  };

  void print()
  {
    for (int i = 0; i < 3; i++)
      array[i].print(); };

  void print_diff(state *prevstate)
  {
    for (int i = 0; i < 3; i++)
      array[i].print_diff(prevstate);
  };
};

  void mu_1__type_9::set_self_ar( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    int l1 = strlen(n1), l2 = strlen(n2);
    strcpy( longname, n1 );
    longname[l1] = '[';
    strcpy( longname+l1+1, n2 );
    longname[l1+l2+1] = ']';
    longname[l1+l2+2] = 0;
    set_self( longname, os );
  };
  void mu_1__type_9::set_self_2( const char *n1, const char *n2, int os ) {
    if (n1 == NULL) {set_self(NULL, 0); return;}
    strcpy( longname, n1 );
    strcat( longname, n2 );
    set_self( longname, os );
  };
void mu_1__type_9::set_self( const char *n, int os)
  {
    int i=0;
    name = (char *)n;

if (n) array[i].set_self_ar(n,"Proc_1", i * 24 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_2", i * 24 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
if (n) array[i].set_self_ar(n,"Proc_3", i * 24 + os); else array[i].set_self_ar(NULL, NULL, 0); i++;
}
mu_1__type_9::~mu_1__type_9()
{
}
/*** end array declaration ***/
mu_1__type_9 mu_1__type_9_undefined_var;

const int mu_ProcCount = 3;
const int mu_ValueCount = 2;
const int mu_HopCount = 2;
const int mu_Proc_1 = 1;
const int mu_Proc_2 = 2;
const int mu_Proc_3 = 3;
const int mu_Value_1 = 4;
const int mu_Value_2 = 5;
const int mu_HomeType = 6;
const int mu_store = 7;
const int mu_load = 8;
const int mu_evict = 9;
const int mu_GetMsg = 10;
const int mu_PutMsg = 11;
const int mu_DataRespMsg = 12;
const int mu_H_I = 13;
const int mu_H_V = 14;
const int mu_P_I = 15;
const int mu_P_IVD = 16;
const int mu_P_V = 17;
const int mu_ci_store = 18;
const int mu_ci_load = 19;
const int mu_ci_evict = 20;
/*** Variable declaration ***/
mu_1_Node mu_cur_node("cur_node",0);

/*** Variable declaration ***/
mu_1__type_2 mu_msg_imm_sent_set("msg_imm_sent_set",8);

/*** Variable declaration ***/
mu_1_MessageType mu_prevMsg("prevMsg",32);

/*** Variable declaration ***/
mu_0_boolean mu_tracked("tracked",40);

/*** Variable declaration ***/
mu_0_boolean mu_start("start",48);

/*** Variable declaration ***/
mu_1__type_3 mu_cur_idx("cur_idx",56);

/*** Variable declaration ***/
mu_1__type_4 mu_tar("tar",64);

/*** Variable declaration ***/
mu_1_ProcStateEnum mu_prevProcs("prevProcs",72);

/*** Variable declaration ***/
mu_1_CoreReq mu_prevProcReq("prevProcReq",80);

/*** Variable declaration ***/
mu_1_Proc mu_selc("selc",104);

/*** Variable declaration ***/
mu_1__type_5 mu_match("match",112);

/*** Variable declaration ***/
mu_1_HomeState mu_HomeNode("HomeNode",120);

/*** Variable declaration ***/
mu_1__type_6 mu_Procs("Procs",136);

/*** Variable declaration ***/
mu_1_Value mu_LastWrite("LastWrite",184);

/*** Variable declaration ***/
mu_1_Value mu_MainMemory("MainMemory",192);

/*** Variable declaration ***/
mu_1_Message mu_gBuf("gBuf",200);

/*** Variable declaration ***/
mu_1__type_7 mu_ackBus("ackBus",232);

/*** Variable declaration ***/
mu_1__type_8 mu_msgBuf("msgBuf",264);

/*** Variable declaration ***/
mu_0_boolean mu_msgBufNonEmpty("msgBufNonEmpty",392);

/*** Variable declaration ***/
mu_1__type_9 mu_curRequsts("curRequsts",400);

void mu_book_keep(const mu_1_Node& mu_m)
{
/*** Variable declaration ***/
mu_1_ProcStateEnum mu_cur_state("cur_state",0);

/*** Variable declaration ***/
mu_0_boolean mu_in_stable_state("in_stable_state",8);

if (mu_Procs[mu_selc].mu_state.isundefined())
  mu_cur_state.undefine();
else
  mu_cur_state = mu_Procs[mu_selc].mu_state;
bool mu__boolexpr10;
  if ((mu_cur_state) == (mu_P_I)) mu__boolexpr10 = TRUE ;
  else {
  mu__boolexpr10 = ((mu_cur_state) == (mu_P_V)) ; 
}
mu_in_stable_state = mu__boolexpr10;
if ( mu_start )
{
if ( (mu_prevProcs) != (mu_cur_state) )
{
switch ((int) mu_match) {
case 0:
bool mu__boolexpr11;
bool mu__boolexpr12;
  if (!((mu_msg_imm_sent_set[mu_GetMsg]) == (mu_false))) mu__boolexpr12 = FALSE ;
  else {
  mu__boolexpr12 = ((mu_msg_imm_sent_set[mu_PutMsg]) == (mu_false)) ; 
}
  if (!(mu__boolexpr12)) mu__boolexpr11 = FALSE ;
  else {
  mu__boolexpr11 = ((mu_msg_imm_sent_set[mu_DataRespMsg]) == (mu_true)) ; 
}
if ( mu__boolexpr11 )
{
mu_match = (mu_match) + (1);
}
else
{
mu_match = 2;
}
break;
}
{
for(int mu_tmpm = 10; mu_tmpm <= 12; mu_tmpm++) {
mu_msg_imm_sent_set[mu_tmpm] = mu_false;
};
};
}
if ( (mu_prevProcs) != (mu_cur_state) )
{
if ( (mu_cur_idx) <= (1) )
{
bool mu__boolexpr13;
  if (!((mu_cur_idx) < (1))) mu__boolexpr13 = FALSE ;
  else {
  mu__boolexpr13 = ((mu_cur_state) == (mu_tar[mu_cur_idx])) ; 
}
if ( mu__boolexpr13 )
{
mu_cur_idx = (mu_cur_idx) + (1);
}
else
{
mu_cur_idx = 2;
}
}
}
if ( mu_in_stable_state )
{
mu_start = mu_false;
}
}
if (mu_m.isundefined())
  mu_cur_node.undefine();
else
  mu_cur_node = mu_m;
mu_prevMsg.undefine();
if (mu_Procs[mu_selc].mu_state.isundefined())
  mu_prevProcs.undefine();
else
  mu_prevProcs = mu_Procs[mu_selc].mu_state;
mu_prevProcReq.undefine();
};
/*** end procedure declaration ***/

void mu_get_evict_req(const mu_1_Proc& mu_m)
{
if ( (mu_m) == (mu_selc) )
{
mu_prevProcReq.mu_tp = mu_ci_evict;
mu_prevProcReq.mu_cl.undefine();
mu_prevProcReq.mu_vld = mu_true;
}
};
/*** end procedure declaration ***/

void mu_get_store_req(const mu_1_Proc& mu_m, const mu_1_Value& mu_cl)
{
if ( (mu_m) == (mu_selc) )
{
mu_prevProcReq.mu_tp = mu_ci_store;
if (mu_cl.isundefined())
  mu_prevProcReq.mu_cl.undefine();
else
  mu_prevProcReq.mu_cl = mu_cl;
mu_prevProcReq.mu_vld = mu_true;
}
};
/*** end procedure declaration ***/

void mu_get_load_req(const mu_1_Proc& mu_m)
{
if ( (mu_m) == (mu_selc) )
{
mu_prevProcReq.mu_tp = mu_ci_load;
mu_prevProcReq.mu_cl.undefine();
mu_prevProcReq.mu_vld = mu_true;
}
};
/*** end procedure declaration ***/

void mu_send_req(const mu_1_MessageType& mu_mtype, const mu_1_Node& mu_src, const mu_1_Node& mu_dst, const mu_1_Value& mu_val)
{
if ( !(mu_gBuf.mu_src.isundefined()) ) Error.Error("Assertion failed: ??");
if ( !(!(mu_msgBufNonEmpty)) ) Error.Error("Assertion failed: ??? still response");
if (mu_mtype.isundefined())
  mu_gBuf.mu_mtype.undefine();
else
  mu_gBuf.mu_mtype = mu_mtype;
if (mu_src.isundefined())
  mu_gBuf.mu_src.undefine();
else
  mu_gBuf.mu_src = mu_src;
if (mu_dst.isundefined())
  mu_gBuf.mu_dst.undefine();
else
  mu_gBuf.mu_dst = mu_dst;
if (mu_val.isundefined())
  mu_gBuf.mu_val.undefine();
else
  mu_gBuf.mu_val = mu_val;
{
for(int mu_n = 1; mu_n <= 6; mu_n++)
  if (( ( mu_n >= 1 ) && ( mu_n <= 3 ) )|| ( ( mu_n >= 6 ) && ( mu_n <= 6 ) )) {
mu_ackBus[mu_n] = mu_false;
};
};
bool mu__boolexpr14;
  if (!(!(mu_cur_node.isundefined()))) mu__boolexpr14 = FALSE ;
  else {
  mu__boolexpr14 = ((mu_cur_node) == (mu_selc)) ; 
}
if ( mu__boolexpr14 )
{
if (mu_gBuf.mu_mtype.isundefined())
  mu_prevMsg.undefine();
else
  mu_prevMsg = mu_gBuf.mu_mtype;
}
bool mu__boolexpr15;
bool mu__boolexpr16;
  if (!(mu_start)) mu__boolexpr16 = FALSE ;
  else {
  mu__boolexpr16 = (!(mu_cur_node.isundefined())) ; 
}
  if (!(mu__boolexpr16)) mu__boolexpr15 = FALSE ;
  else {
  mu__boolexpr15 = ((mu_cur_node) == (mu_selc)) ; 
}
if ( mu__boolexpr15 )
{
mu_msg_imm_sent_set[mu_gBuf.mu_mtype] = mu_true;
}
};
/*** end procedure declaration ***/

void mu_send_resp(const mu_1_MessageType& mu_mtype, const mu_1_Node& mu_src, const mu_1_Node& mu_dst, const mu_1_Value& mu_val)
{
/*** Variable declaration ***/
mu_1_Message mu_msg("msg",0);

if ( !(!(mu_msgBufNonEmpty)) ) Error.Error("Assertion failed: ??? still response");
if ( !(!(mu_gBuf.mu_src.isundefined())) ) Error.Error("Assertion failed: ? no txn?");
if (mu_mtype.isundefined())
  mu_msg.mu_mtype.undefine();
else
  mu_msg.mu_mtype = mu_mtype;
if (mu_src.isundefined())
  mu_msg.mu_src.undefine();
else
  mu_msg.mu_src = mu_src;
if (mu_dst.isundefined())
  mu_msg.mu_dst.undefine();
else
  mu_msg.mu_dst = mu_dst;
if (mu_val.isundefined())
  mu_msg.mu_val.undefine();
else
  mu_msg.mu_val = mu_val;
mu_msgBuf[mu_src] = mu_msg;
mu_msgBufNonEmpty = mu_true;
bool mu__boolexpr17;
  if (!(!(mu_cur_node.isundefined()))) mu__boolexpr17 = FALSE ;
  else {
  mu__boolexpr17 = ((mu_cur_node) == (mu_selc)) ; 
}
if ( mu__boolexpr17 )
{
if (mu_msg.mu_mtype.isundefined())
  mu_prevMsg.undefine();
else
  mu_prevMsg = mu_msg.mu_mtype;
}
bool mu__boolexpr18;
bool mu__boolexpr19;
  if (!(mu_start)) mu__boolexpr19 = FALSE ;
  else {
  mu__boolexpr19 = (!(mu_cur_node.isundefined())) ; 
}
  if (!(mu__boolexpr19)) mu__boolexpr18 = FALSE ;
  else {
  mu__boolexpr18 = ((mu_cur_node) == (mu_selc)) ; 
}
if ( mu__boolexpr18 )
{
mu_msg_imm_sent_set[mu_msg.mu_mtype] = mu_true;
}
};
/*** end procedure declaration ***/

void mu_HomeReceive(mu_1_Message& mu_msg)
{
switch ((int) mu_HomeNode.mu_state) {
case mu_H_I:
switch ((int) mu_msg.mu_mtype) {
case mu_GetMsg:
mu_HomeNode.mu_state = mu_H_V;
if (mu_MainMemory.isundefined())
  mu_HomeNode.mu_val.undefine();
else
  mu_HomeNode.mu_val = mu_MainMemory;
mu_send_resp ( mu_DataRespMsg, (int)mu_HomeType, mu_msg.mu_src, mu_HomeNode.mu_val );
break;
default:
Error.Error("Error: Unhandled message type!");
break;
}
break;
case mu_H_V:
switch ((int) mu_msg.mu_mtype) {
case mu_PutMsg:
mu_HomeNode.mu_state = mu_H_I;
if (mu_msg.mu_val.isundefined())
  mu_HomeNode.mu_val.undefine();
else
  mu_HomeNode.mu_val = mu_msg.mu_val;
if (mu_msg.mu_val.isundefined())
  mu_MainMemory.undefine();
else
  mu_MainMemory = mu_msg.mu_val;
break;
}
break;
}
};
/*** end procedure declaration ***/

void mu_ProcReceive(mu_1_Message& mu_msg, const mu_1_Proc& mu_p)
{
{
  mu_1_ProcStateEnum& mu_ps = mu_Procs[mu_p].mu_state;
{
  mu_1_Value& mu_pv = mu_Procs[mu_p].mu_val;
switch ((int) mu_ps) {
case mu_P_I:
if ( (mu_msg.mu_mtype) == (mu_GetMsg) )
{
if ( !((mu_msg.mu_src) != (mu_p)) ) Error.Error("Assertion failed: Huh?");
}
break;
case mu_P_IVD:
switch ((int) mu_msg.mu_mtype) {
case mu_DataRespMsg:
if ( !((mu_msg.mu_dst) == (mu_p)) ) Error.Error("Assertion failed: Huh not for me?");
if (mu_msg.mu_val.isundefined())
  mu_pv.undefine();
else
  mu_pv = mu_msg.mu_val;
mu_ps = mu_P_V;
break;
case mu_GetMsg:
if ( !((mu_msg.mu_src) == (mu_p)) ) Error.Error("Assertion failed: not from me?");
break;
default:
Error.Error("Error: Huh?? I'm in active transaction?");
break;
}
break;
case mu_P_V:
switch ((int) mu_msg.mu_mtype) {
case mu_GetMsg:
mu_send_resp ( mu_DataRespMsg, (int)mu_p, mu_msg.mu_src, mu_pv );
mu_ps = mu_P_I;
break;
default:
Error.Error("Error: Huh? I hold it");
break;
}
break;
}
}
}
};
/*** end procedure declaration ***/





/********************
  The world
 ********************/
void world_class::clear()
{
  mu_cur_node.clear();
  mu_msg_imm_sent_set.clear();
  mu_prevMsg.clear();
  mu_tracked.clear();
  mu_start.clear();
  mu_cur_idx.clear();
  mu_tar.clear();
  mu_prevProcs.clear();
  mu_prevProcReq.clear();
  mu_selc.clear();
  mu_match.clear();
  mu_HomeNode.clear();
  mu_Procs.clear();
  mu_LastWrite.clear();
  mu_MainMemory.clear();
  mu_gBuf.clear();
  mu_ackBus.clear();
  mu_msgBuf.clear();
  mu_msgBufNonEmpty.clear();
  mu_curRequsts.clear();
}
void world_class::undefine()
{
  mu_cur_node.undefine();
  mu_msg_imm_sent_set.undefine();
  mu_prevMsg.undefine();
  mu_tracked.undefine();
  mu_start.undefine();
  mu_cur_idx.undefine();
  mu_tar.undefine();
  mu_prevProcs.undefine();
  mu_prevProcReq.undefine();
  mu_selc.undefine();
  mu_match.undefine();
  mu_HomeNode.undefine();
  mu_Procs.undefine();
  mu_LastWrite.undefine();
  mu_MainMemory.undefine();
  mu_gBuf.undefine();
  mu_ackBus.undefine();
  mu_msgBuf.undefine();
  mu_msgBufNonEmpty.undefine();
  mu_curRequsts.undefine();
}
void world_class::reset()
{
  mu_cur_node.reset();
  mu_msg_imm_sent_set.reset();
  mu_prevMsg.reset();
  mu_tracked.reset();
  mu_start.reset();
  mu_cur_idx.reset();
  mu_tar.reset();
  mu_prevProcs.reset();
  mu_prevProcReq.reset();
  mu_selc.reset();
  mu_match.reset();
  mu_HomeNode.reset();
  mu_Procs.reset();
  mu_LastWrite.reset();
  mu_MainMemory.reset();
  mu_gBuf.reset();
  mu_ackBus.reset();
  mu_msgBuf.reset();
  mu_msgBufNonEmpty.reset();
  mu_curRequsts.reset();
}
void world_class::print()
{
  static int num_calls = 0; /* to ward off recursive calls. */
  if ( num_calls == 0 ) {
    num_calls++;
  mu_cur_node.print();
  mu_msg_imm_sent_set.print();
  mu_prevMsg.print();
  mu_tracked.print();
  mu_start.print();
  mu_cur_idx.print();
  mu_tar.print();
  mu_prevProcs.print();
  mu_prevProcReq.print();
  mu_selc.print();
  mu_match.print();
  mu_HomeNode.print();
  mu_Procs.print();
  mu_LastWrite.print();
  mu_MainMemory.print();
  mu_gBuf.print();
  mu_ackBus.print();
  mu_msgBuf.print();
  mu_msgBufNonEmpty.print();
  mu_curRequsts.print();
    num_calls--;
}
}
void world_class::print_statistic()
{
  static int num_calls = 0; /* to ward off recursive calls. */
  if ( num_calls == 0 ) {
    num_calls++;
  mu_cur_node.print_statistic();
  mu_msg_imm_sent_set.print_statistic();
  mu_prevMsg.print_statistic();
  mu_tracked.print_statistic();
  mu_start.print_statistic();
  mu_cur_idx.print_statistic();
  mu_tar.print_statistic();
  mu_prevProcs.print_statistic();
  mu_prevProcReq.print_statistic();
  mu_selc.print_statistic();
  mu_match.print_statistic();
  mu_HomeNode.print_statistic();
  mu_Procs.print_statistic();
  mu_LastWrite.print_statistic();
  mu_MainMemory.print_statistic();
  mu_gBuf.print_statistic();
  mu_ackBus.print_statistic();
  mu_msgBuf.print_statistic();
  mu_msgBufNonEmpty.print_statistic();
  mu_curRequsts.print_statistic();
    num_calls--;
}
}
void world_class::print_diff( state *prevstate )
{
  if ( prevstate != NULL )
  {
    mu_cur_node.print_diff(prevstate);
    mu_msg_imm_sent_set.print_diff(prevstate);
    mu_prevMsg.print_diff(prevstate);
    mu_tracked.print_diff(prevstate);
    mu_start.print_diff(prevstate);
    mu_cur_idx.print_diff(prevstate);
    mu_tar.print_diff(prevstate);
    mu_prevProcs.print_diff(prevstate);
    mu_prevProcReq.print_diff(prevstate);
    mu_selc.print_diff(prevstate);
    mu_match.print_diff(prevstate);
    mu_HomeNode.print_diff(prevstate);
    mu_Procs.print_diff(prevstate);
    mu_LastWrite.print_diff(prevstate);
    mu_MainMemory.print_diff(prevstate);
    mu_gBuf.print_diff(prevstate);
    mu_ackBus.print_diff(prevstate);
    mu_msgBuf.print_diff(prevstate);
    mu_msgBufNonEmpty.print_diff(prevstate);
    mu_curRequsts.print_diff(prevstate);
  }
  else
print();
}
void world_class::to_state(state *newstate)
{
  mu_cur_node.to_state( newstate );
  mu_msg_imm_sent_set.to_state( newstate );
  mu_prevMsg.to_state( newstate );
  mu_tracked.to_state( newstate );
  mu_start.to_state( newstate );
  mu_cur_idx.to_state( newstate );
  mu_tar.to_state( newstate );
  mu_prevProcs.to_state( newstate );
  mu_prevProcReq.to_state( newstate );
  mu_selc.to_state( newstate );
  mu_match.to_state( newstate );
  mu_HomeNode.to_state( newstate );
  mu_Procs.to_state( newstate );
  mu_LastWrite.to_state( newstate );
  mu_MainMemory.to_state( newstate );
  mu_gBuf.to_state( newstate );
  mu_ackBus.to_state( newstate );
  mu_msgBuf.to_state( newstate );
  mu_msgBufNonEmpty.to_state( newstate );
  mu_curRequsts.to_state( newstate );
}
void world_class::setstate(state *thestate)
{
}


/********************
  Rule declarations
 ********************/
/******************** RuleBase0 ********************/
class RuleBase0
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    return tsprintf("track_P_V_ci_evict");
  }
  bool Condition(unsigned r)
  {
bool mu__boolexpr20;
bool mu__boolexpr21;
bool mu__boolexpr22;
bool mu__boolexpr23;
  if (!(!(mu_tracked))) mu__boolexpr23 = FALSE ;
  else {
  mu__boolexpr23 = (!(mu_prevProcs.isundefined())) ; 
}
  if (!(mu__boolexpr23)) mu__boolexpr22 = FALSE ;
  else {
  mu__boolexpr22 = ((mu_prevProcs) == (mu_P_V)) ; 
}
  if (!(mu__boolexpr22)) mu__boolexpr21 = FALSE ;
  else {
  mu__boolexpr21 = (!(mu_prevProcReq.mu_tp.isundefined())) ; 
}
  if (!(mu__boolexpr21)) mu__boolexpr20 = FALSE ;
  else {
  mu__boolexpr20 = ((mu_prevProcReq.mu_tp) == (mu_ci_evict)) ; 
}
    return mu__boolexpr20;
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 0;
    while (what_rule < 1 )
      {
	if ( ( TRUE  ) ) {
bool mu__boolexpr24;
bool mu__boolexpr25;
bool mu__boolexpr26;
bool mu__boolexpr27;
  if (!(!(mu_tracked))) mu__boolexpr27 = FALSE ;
  else {
  mu__boolexpr27 = (!(mu_prevProcs.isundefined())) ; 
}
  if (!(mu__boolexpr27)) mu__boolexpr26 = FALSE ;
  else {
  mu__boolexpr26 = ((mu_prevProcs) == (mu_P_V)) ; 
}
  if (!(mu__boolexpr26)) mu__boolexpr25 = FALSE ;
  else {
  mu__boolexpr25 = (!(mu_prevProcReq.mu_tp.isundefined())) ; 
}
  if (!(mu__boolexpr25)) mu__boolexpr24 = FALSE ;
  else {
  mu__boolexpr24 = ((mu_prevProcReq.mu_tp) == (mu_ci_evict)) ; 
}
	      if (mu__boolexpr24) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 0;
    }
  }

  void Code(unsigned r)
  {
mu_start = mu_true;
mu_tracked = mu_true;
if ( !(mu_prevMsg.isundefined()) )
{
mu_msg_imm_sent_set[mu_prevMsg] = mu_true;
}
  };

};
/******************** RuleBase1 ********************/
class RuleBase1
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    return tsprintf("bus_atomic_req");
  }
  bool Condition(unsigned r)
  {
    return !(mu_gBuf.mu_src.isundefined());
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 1;
    while (what_rule < 2 )
      {
	if ( ( TRUE  ) ) {
	      if (!(mu_gBuf.mu_src.isundefined())) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 1;
    }
  }

  void Code(unsigned r)
  {
/*** Variable declaration ***/
mu_0_boolean mu_allAck("allAck",0);

/*** Variable declaration ***/
mu_1_Message mu_nMsg("nMsg",8);

mu_nMsg.undefine();
mu_allAck = mu_true;
{
for(int mu_n = 1; mu_n <= 6; mu_n++)
  if (( ( mu_n >= 1 ) && ( mu_n <= 3 ) )|| ( ( mu_n >= 6 ) && ( mu_n <= 6 ) )) {
bool mu__boolexpr28;
  if (!(mu_allAck)) mu__boolexpr28 = FALSE ;
  else {
  mu__boolexpr28 = (mu_ackBus[mu_n]) ; 
}
mu_allAck = mu__boolexpr28;
};
};
if ( mu_allAck )
{
{
for(int mu_n = 1; mu_n <= 6; mu_n++)
  if (( ( mu_n >= 1 ) && ( mu_n <= 3 ) )|| ( ( mu_n >= 6 ) && ( mu_n <= 6 ) )) {
mu_ackBus[mu_n] = mu_false;
};
};
mu_gBuf.undefine();
if ( mu_msgBufNonEmpty )
{
{
for(int mu_n = 1; mu_n <= 6; mu_n++)
  if (( ( mu_n >= 1 ) && ( mu_n <= 3 ) )|| ( ( mu_n >= 6 ) && ( mu_n <= 6 ) )) {
if ( !(mu_msgBuf[mu_n].mu_src.isundefined()) )
{
if ( !(mu_nMsg.mu_src.isundefined()) ) Error.Error("Assertion failed: there should exist some active txn?");
mu_nMsg = mu_msgBuf[mu_n];
mu_msgBuf[mu_n].undefine();
mu_msgBufNonEmpty = mu_false;
}
};
};
mu_gBuf = mu_nMsg;
if ( !(!(mu_gBuf.mu_src.isundefined())) ) Error.Error("Assertion failed: should be completing...");
}
}
  };

};
/******************** RuleBase2 ********************/
class RuleBase2
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Node mu_n;
    mu_n.unionassign(r % 4);
    r = r / 4;
    return tsprintf("receiveFromBus, n:%s", mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Node mu_n;
    mu_n.unionassign(r % 4);
    r = r / 4;
bool mu__boolexpr29;
  if (!(!(mu_gBuf.mu_src.isundefined()))) mu__boolexpr29 = FALSE ;
  else {
  mu__boolexpr29 = (!(mu_ackBus[mu_n])) ; 
}
    return mu__boolexpr29;
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 2;
    static mu_1_Node mu_n;
    mu_n.unionassign(r % 4);
    r = r / 4;
    while (what_rule < 6 )
      {
	if ( ( TRUE  ) ) {
bool mu__boolexpr30;
  if (!(!(mu_gBuf.mu_src.isundefined()))) mu__boolexpr30 = FALSE ;
  else {
  mu__boolexpr30 = (!(mu_ackBus[mu_n])) ; 
}
	      if (mu__boolexpr30) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 2;
    mu_n.unionassign(r % 4);
    r = r / 4;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Node mu_n;
    mu_n.unionassign(r % 4);
    r = r / 4;
mu_book_keep ( mu_n );
mu_ackBus[mu_n] = mu_true;
if ( (mu_n>=6 && mu_n<=6) )
{
mu_HomeReceive ( mu_gBuf );
}
else
{
mu_ProcReceive ( mu_gBuf, (int)mu_n );
}
  };

};
/******************** RuleBase3 ********************/
class RuleBase3
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    return tsprintf("evict_P_V, n:%s", mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr31;
bool mu__boolexpr32;
  if (!((mu_p.mu_state) == (mu_P_V))) mu__boolexpr32 = FALSE ;
  else {
  mu__boolexpr32 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr32)) mu__boolexpr31 = FALSE ;
  else {
  mu__boolexpr31 = (mu_gBuf.mu_src.isundefined()) ; 
}
    return mu__boolexpr31;
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 6;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    while (what_rule < 9 )
      {
	if ( ( TRUE  ) ) {
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr33;
bool mu__boolexpr34;
  if (!((mu_p.mu_state) == (mu_P_V))) mu__boolexpr34 = FALSE ;
  else {
  mu__boolexpr34 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr34)) mu__boolexpr33 = FALSE ;
  else {
  mu__boolexpr33 = (mu_gBuf.mu_src.isundefined()) ; 
}
	      if (mu__boolexpr33) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 6;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
mu_book_keep ( (int)mu_n );
mu_get_evict_req ( mu_n );
mu_send_req ( mu_PutMsg, (int)mu_n, (int)mu_HomeType, mu_p.mu_val );
mu_p.mu_state = mu_P_I;
  };

};
/******************** RuleBase4 ********************/
class RuleBase4
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    return tsprintf("store_P_V, v:%s, n:%s", mu_v.Name(), mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
    return (mu_p.mu_state) == (mu_P_V);
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 9;
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    while (what_rule < 15 )
      {
	if ( ( TRUE  ) ) {
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
	      if ((mu_p.mu_state) == (mu_P_V)) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 2;
	}
	else
	  what_rule += 2;
    r = what_rule - 9;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
mu_book_keep ( (int)mu_n );
mu_get_store_req ( mu_n, mu_v );
mu_p.mu_val = mu_v;
mu_LastWrite = mu_v;
  };

};
/******************** RuleBase5 ********************/
class RuleBase5
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    return tsprintf("load_P_V, n:%s", mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
    return (mu_p.mu_state) == (mu_P_V);
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 15;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    while (what_rule < 18 )
      {
	if ( ( TRUE  ) ) {
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
	      if ((mu_p.mu_state) == (mu_P_V)) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 15;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
mu_book_keep ( (int)mu_n );
mu_get_load_req ( mu_n );
mu_p.mu_state = mu_P_V;
  };

};
/******************** RuleBase6 ********************/
class RuleBase6
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    return tsprintf("store_P_I, v:%s, n:%s", mu_v.Name(), mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr35;
bool mu__boolexpr36;
  if (!((mu_p.mu_state) == (mu_P_I))) mu__boolexpr36 = FALSE ;
  else {
  mu__boolexpr36 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr36)) mu__boolexpr35 = FALSE ;
  else {
  mu__boolexpr35 = (mu_gBuf.mu_src.isundefined()) ; 
}
    return mu__boolexpr35;
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 18;
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    while (what_rule < 24 )
      {
	if ( ( TRUE  ) ) {
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr37;
bool mu__boolexpr38;
  if (!((mu_p.mu_state) == (mu_P_I))) mu__boolexpr38 = FALSE ;
  else {
  mu__boolexpr38 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr38)) mu__boolexpr37 = FALSE ;
  else {
  mu__boolexpr37 = (mu_gBuf.mu_src.isundefined()) ; 
}
	      if (mu__boolexpr37) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 2;
	}
	else
	  what_rule += 2;
    r = what_rule - 18;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Value mu_v;
    mu_v.value((r % 2) + 4);
    r = r / 2;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
mu_book_keep ( (int)mu_n );
mu_get_store_req ( mu_n, mu_v );
mu_curRequsts[mu_n].mu_vld = mu_true;
mu_curRequsts[mu_n].mu_tp = mu_store;
mu_send_req ( mu_GetMsg, (int)mu_n, mu_1_Node_undefined_var, mu_1_Value_undefined_var );
mu_p.mu_state = mu_P_IVD;
mu_p.mu_val = mu_v;
  };

};
/******************** RuleBase7 ********************/
class RuleBase7
{
public:
  int Priority()
  {
    return 0;
  }
  char * Name(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    return tsprintf("load_P_I, n:%s", mu_n.Name());
  }
  bool Condition(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr39;
bool mu__boolexpr40;
  if (!((mu_p.mu_state) == (mu_P_I))) mu__boolexpr40 = FALSE ;
  else {
  mu__boolexpr40 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr40)) mu__boolexpr39 = FALSE ;
  else {
  mu__boolexpr39 = (mu_gBuf.mu_src.isundefined()) ; 
}
    return mu__boolexpr39;
  }

  void NextRule(unsigned & what_rule)
  {
    unsigned r = what_rule - 24;
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    while (what_rule < 27 )
      {
	if ( ( TRUE  ) ) {
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
bool mu__boolexpr41;
bool mu__boolexpr42;
  if (!((mu_p.mu_state) == (mu_P_I))) mu__boolexpr42 = FALSE ;
  else {
  mu__boolexpr42 = (!(mu_msgBufNonEmpty)) ; 
}
  if (!(mu__boolexpr42)) mu__boolexpr41 = FALSE ;
  else {
  mu__boolexpr41 = (mu_gBuf.mu_src.isundefined()) ; 
}
	      if (mu__boolexpr41) {
		if ( ( TRUE  ) )
		  return;
		else
		  what_rule++;
	      }
	      else
		what_rule += 1;
	}
	else
	  what_rule += 1;
    r = what_rule - 24;
    mu_n.value((r % 3) + 1);
    r = r / 3;
    }
  }

  void Code(unsigned r)
  {
    static mu_1_Proc mu_n;
    mu_n.value((r % 3) + 1);
    r = r / 3;
  mu_1_ProcState& mu_p = mu_Procs[mu_n];
mu_book_keep ( (int)mu_n );
mu_get_load_req ( mu_n );
mu_send_req ( mu_GetMsg, (int)mu_n, mu_1_Node_undefined_var, mu_1_Value_undefined_var );
mu_p.mu_state = mu_P_IVD;
  };

};
class NextStateGenerator
{
  RuleBase0 R0;
  RuleBase1 R1;
  RuleBase2 R2;
  RuleBase3 R3;
  RuleBase4 R4;
  RuleBase5 R5;
  RuleBase6 R6;
  RuleBase7 R7;
public:
void SetNextEnabledRule(unsigned & what_rule)
{
  category = CONDITION;
  if (what_rule<1)
    { R0.NextRule(what_rule);
      if (what_rule<1) return; }
  if (what_rule>=1 && what_rule<2)
    { R1.NextRule(what_rule);
      if (what_rule<2) return; }
  if (what_rule>=2 && what_rule<6)
    { R2.NextRule(what_rule);
      if (what_rule<6) return; }
  if (what_rule>=6 && what_rule<9)
    { R3.NextRule(what_rule);
      if (what_rule<9) return; }
  if (what_rule>=9 && what_rule<15)
    { R4.NextRule(what_rule);
      if (what_rule<15) return; }
  if (what_rule>=15 && what_rule<18)
    { R5.NextRule(what_rule);
      if (what_rule<18) return; }
  if (what_rule>=18 && what_rule<24)
    { R6.NextRule(what_rule);
      if (what_rule<24) return; }
  if (what_rule>=24 && what_rule<27)
    { R7.NextRule(what_rule);
      if (what_rule<27) return; }
}
bool Condition(unsigned r)
{
  category = CONDITION;
  if (r<=0) return R0.Condition(r-0);
  if (r>=1 && r<=1) return R1.Condition(r-1);
  if (r>=2 && r<=5) return R2.Condition(r-2);
  if (r>=6 && r<=8) return R3.Condition(r-6);
  if (r>=9 && r<=14) return R4.Condition(r-9);
  if (r>=15 && r<=17) return R5.Condition(r-15);
  if (r>=18 && r<=23) return R6.Condition(r-18);
  if (r>=24 && r<=26) return R7.Condition(r-24);
Error.Notrace("Internal: NextStateGenerator -- checking condition for nonexisting rule.");
return 0;}
void Code(unsigned r)
{
  if (r<=0) { R0.Code(r-0); return; } 
  if (r>=1 && r<=1) { R1.Code(r-1); return; } 
  if (r>=2 && r<=5) { R2.Code(r-2); return; } 
  if (r>=6 && r<=8) { R3.Code(r-6); return; } 
  if (r>=9 && r<=14) { R4.Code(r-9); return; } 
  if (r>=15 && r<=17) { R5.Code(r-15); return; } 
  if (r>=18 && r<=23) { R6.Code(r-18); return; } 
  if (r>=24 && r<=26) { R7.Code(r-24); return; } 
}
int Priority(unsigned short r)
{
  if (r<=0) { return R0.Priority(); } 
  if (r>=1 && r<=1) { return R1.Priority(); } 
  if (r>=2 && r<=5) { return R2.Priority(); } 
  if (r>=6 && r<=8) { return R3.Priority(); } 
  if (r>=9 && r<=14) { return R4.Priority(); } 
  if (r>=15 && r<=17) { return R5.Priority(); } 
  if (r>=18 && r<=23) { return R6.Priority(); } 
  if (r>=24 && r<=26) { return R7.Priority(); } 
return 0;}
char * Name(unsigned r)
{
  if (r<=0) return R0.Name(r-0);
  if (r>=1 && r<=1) return R1.Name(r-1);
  if (r>=2 && r<=5) return R2.Name(r-2);
  if (r>=6 && r<=8) return R3.Name(r-6);
  if (r>=9 && r<=14) return R4.Name(r-9);
  if (r>=15 && r<=17) return R5.Name(r-15);
  if (r>=18 && r<=23) return R6.Name(r-18);
  if (r>=24 && r<=26) return R7.Name(r-24);
  return NULL;
}
};
const unsigned numrules = 27;

/********************
  parameter
 ********************/
#define RULES_IN_WORLD 27


/********************
  Startstate records
 ********************/
/******************** StartStateBase0 ********************/
class StartStateBase0
{
public:
  char * Name(unsigned short r)
  {
    return tsprintf("Startstate 0");
  }
  void Code(unsigned short r)
  {
mu_curRequsts.undefine();
mu_HomeNode.mu_state = mu_H_I;
{
for(int mu_v = 4; mu_v <= 5; mu_v++) {
mu_MainMemory = mu_v;
};
};
if (mu_MainMemory.isundefined())
  mu_LastWrite.undefine();
else
  mu_LastWrite = mu_MainMemory;
{
for(int mu_i = 1; mu_i <= 3; mu_i++) {
mu_Procs[mu_i].mu_state = mu_P_I;
mu_Procs[mu_i].mu_val.undefine();
};
};
mu_gBuf.undefine();
{
for(int mu_n = 1; mu_n <= 6; mu_n++)
  if (( ( mu_n >= 1 ) && ( mu_n <= 3 ) )|| ( ( mu_n >= 6 ) && ( mu_n <= 6 ) )) {
mu_ackBus[mu_n] = mu_false;
};
};
mu_msgBuf.undefine();
mu_msgBufNonEmpty = mu_false;
mu_cur_node.undefine();
{
for(int mu_m = 10; mu_m <= 12; mu_m++) {
mu_msg_imm_sent_set[mu_m] = mu_false;
};
};
mu_tracked = mu_false;
mu_start = mu_false;
mu_cur_idx = 0;
mu_tar[0] = mu_P_I;
mu_prevProcReq.undefine();
{
for(int mu_n = 1; mu_n <= 3; mu_n++) {
mu_selc = mu_n;
};
};
mu_match = 0;
  };

};
class StartStateGenerator
{
  StartStateBase0 S0;
public:
void Code(unsigned short r)
{
  if (r<=0) { S0.Code(r-0); return; }
}
char * Name(unsigned short r)
{
  if (r<=0) return S0.Name(r-0);
  return NULL;
}
};
const rulerec startstates[] = {
{ NULL, NULL, NULL, FALSE},
};
unsigned short StartStateManager::numstartstates = 1;

/********************
  Invariant records
 ********************/
int mu__invariant_43() // Invariant "P_V_ci_evict_rset_0"
{
bool mu__boolexpr44;
bool mu__boolexpr45;
bool mu__boolexpr46;
  if (!(mu_tracked)) mu__boolexpr46 = FALSE ;
  else {
  mu__boolexpr46 = (!(mu_start)) ; 
}
  if (!(mu__boolexpr46)) mu__boolexpr45 = FALSE ;
  else {
  mu__boolexpr45 = ((mu_cur_idx) == (1)) ; 
}
  if (!(mu__boolexpr45)) mu__boolexpr44 = TRUE ;
  else {
  mu__boolexpr44 = ((mu_match) != (1)) ; 
}
return mu__boolexpr44;
};

bool mu__condition_47() // Condition for Rule "P_V_ci_evict_rset_0"
{
  return mu__invariant_43( );
}

/**** end rule declaration ****/

int mu__invariant_48() // Invariant "swmr"
{
bool mu__quant49; 
mu__quant49 = TRUE;
{
for(int mu_c1 = 1; mu_c1 <= 3; mu_c1++) {
bool mu__quant50; 
mu__quant50 = TRUE;
{
for(int mu_c2 = 1; mu_c2 <= 3; mu_c2++) {
bool mu__boolexpr51;
bool mu__boolexpr52;
  if (!((mu_c1) != (mu_c2))) mu__boolexpr52 = FALSE ;
  else {
  mu__boolexpr52 = ((mu_Procs[mu_c1].mu_state) == (mu_P_V)) ; 
}
  if (!(mu__boolexpr52)) mu__boolexpr51 = TRUE ;
  else {
  mu__boolexpr51 = ((mu_Procs[mu_c2].mu_state) != (mu_P_V)) ; 
}
if ( !(mu__boolexpr51) )
  { mu__quant50 = FALSE; break; }
};
};
if ( !(mu__quant50) )
  { mu__quant49 = FALSE; break; }
};
};
return mu__quant49;
};

bool mu__condition_53() // Condition for Rule "swmr"
{
  return mu__invariant_48( );
}

/**** end rule declaration ****/

int mu__invariant_54() // Invariant "values in valid state match last write"
{
bool mu__quant55; 
mu__quant55 = TRUE;
{
for(int mu_n = 1; mu_n <= 3; mu_n++) {
bool mu__boolexpr56;
  if (!((mu_Procs[mu_n].mu_state) == (mu_P_V))) mu__boolexpr56 = TRUE ;
  else {
  mu__boolexpr56 = ((mu_Procs[mu_n].mu_val) == (mu_LastWrite)) ; 
}
if ( !(mu__boolexpr56) )
  { mu__quant55 = FALSE; break; }
};
};
return mu__quant55;
};

bool mu__condition_57() // Condition for Rule "values in valid state match last write"
{
  return mu__invariant_54( );
}

/**** end rule declaration ****/

int mu__invariant_58() // Invariant "value in memory matches value of last write, when invalid"
{
bool mu__boolexpr59;
  if (!((mu_HomeNode.mu_state) == (mu_H_I))) mu__boolexpr59 = TRUE ;
  else {
  mu__boolexpr59 = ((mu_MainMemory) == (mu_LastWrite)) ; 
}
return mu__boolexpr59;
};

bool mu__condition_60() // Condition for Rule "value in memory matches value of last write, when invalid"
{
  return mu__invariant_58( );
}

/**** end rule declaration ****/

int mu__invariant_61() // Invariant "Invalid implies empty owner"
{
bool mu__boolexpr62;
  if (!((mu_HomeNode.mu_state) == (mu_H_I))) mu__boolexpr62 = TRUE ;
  else {
bool mu__quant63; 
mu__quant63 = TRUE;
{
for(int mu_n = 1; mu_n <= 3; mu_n++) {
if ( !(!((mu_Procs[mu_n].mu_state) == (mu_P_V))) )
  { mu__quant63 = FALSE; break; }
};
};
  mu__boolexpr62 = (mu__quant63) ; 
}
return mu__boolexpr62;
};

bool mu__condition_64() // Condition for Rule "Invalid implies empty owner"
{
  return mu__invariant_61( );
}

/**** end rule declaration ****/

const rulerec invariants[] = {
{"Invalid implies empty owner", &mu__condition_64, NULL, },
{"value in memory matches value of last write, when invalid", &mu__condition_60, NULL, },
{"values in valid state match last write", &mu__condition_57, NULL, },
{"swmr", &mu__condition_53, NULL, },
{"P_V_ci_evict_rset_0", &mu__condition_47, NULL, },
};
const unsigned short numinvariants = 5;

/********************
  Normal/Canonicalization for scalarset
 ********************/
/*
match:NoScalarset
prevProcs:NoScalarset
tracked:NoScalarset
msg_imm_sent_set:NoScalarset
prevMsg:NoScalarset
start:NoScalarset
cur_idx:NoScalarset
tar:NoScalarset
msgBufNonEmpty:NoScalarset
gBuf:ScalarsetVariable
LastWrite:ScalarsetVariable
selc:ScalarsetVariable
cur_node:ScalarsetVariable
prevProcReq:ScalarsetVariable
HomeNode:ScalarsetVariable
MainMemory:ScalarsetVariable
ackBus:ScalarsetArrayOfFree
msgBuf:ScalarsetArrayOfScalarset
Procs:ScalarsetArrayOfScalarset
curRequsts:ScalarsetArrayOfScalarset
*/

/********************
Code for symmetry
 ********************/

/********************
 Permutation Set Class
 ********************/
class PermSet
{
public:
  // book keeping
  enum PresentationType {Simple, Explicit};
  PresentationType Presentation;

  void ResetToSimple();
  void ResetToExplicit();
  void SimpleToExplicit();
  void SimpleToOne();
  bool NextPermutation();

  void Print_in_size()
  { int ret=0; for (int i=0; i<count; i++) if (in[i]) ret++; cout << "in_size:" << ret << "\n"; }


  /********************
   Simple and efficient representation
   ********************/
  int class_mu_1_Value[2];
  int undefined_class_mu_1_Value;// has the highest class number

  void Print_class_mu_1_Value();
  bool OnlyOneRemain_mu_1_Value;
  bool MTO_class_mu_1_Value()
  {
    int i,j;
    if (OnlyOneRemain_mu_1_Value)
      return FALSE;
    for (i=0; i<2; i++)
      for (j=0; j<2; j++)
        if (i!=j && class_mu_1_Value[i]== class_mu_1_Value[j])
	    return TRUE;
    OnlyOneRemain_mu_1_Value = TRUE;
    return FALSE;
  }
  int class_mu_1_Proc[3];
  int undefined_class_mu_1_Proc;// has the highest class number

  void Print_class_mu_1_Proc();
  bool OnlyOneRemain_mu_1_Proc;
  bool MTO_class_mu_1_Proc()
  {
    int i,j;
    if (OnlyOneRemain_mu_1_Proc)
      return FALSE;
    for (i=0; i<3; i++)
      for (j=0; j<3; j++)
        if (i!=j && class_mu_1_Proc[i]== class_mu_1_Proc[j])
	    return TRUE;
    OnlyOneRemain_mu_1_Proc = TRUE;
    return FALSE;
  }
  bool AlreadyOnlyOneRemain;
  bool MoreThanOneRemain();


  /********************
   Explicit representation
  ********************/
  unsigned long size;
  unsigned long count;
  // in will be of product of factorial sizes for fast canonicalize
  // in will be of size 1 for reduced local memory canonicalize
  bool * in;

  // auxiliary for explicit representation

  // in/perm/revperm will be of factorial size for fast canonicalize
  // they will be of size 1 for reduced local memory canonicalize
  // second range will be size of the scalarset
  int * in_mu_1_Value;
  typedef int arr_mu_1_Value[2];
  arr_mu_1_Value * perm_mu_1_Value;
  arr_mu_1_Value * revperm_mu_1_Value;

  int size_mu_1_Value[2];
  bool reversed_sorted_mu_1_Value(int start, int end);
  void reverse_reversed_mu_1_Value(int start, int end);

  int * in_mu_1_Proc;
  typedef int arr_mu_1_Proc[3];
  arr_mu_1_Proc * perm_mu_1_Proc;
  arr_mu_1_Proc * revperm_mu_1_Proc;

  int size_mu_1_Proc[3];
  bool reversed_sorted_mu_1_Proc(int start, int end);
  void reverse_reversed_mu_1_Proc(int start, int end);

  // procedure for explicit representation
  bool ok0(mu_1_Value* perm, int size, mu_1_Value k);
  void GenPerm0(mu_1_Value* perm, int size, unsigned long& index);

  bool ok1(mu_1_Proc* perm, int size, mu_1_Proc k);
  void GenPerm1(mu_1_Proc* perm, int size, unsigned long& index);

  // General procedure
  PermSet();
  bool In(int i) const { return in[i]; };
  void Add(int i) { for (int j=0; j<i; j++) in[j] = FALSE;};
  void Remove(int i) { in[i] = FALSE; };
};
void PermSet::Print_class_mu_1_Value()
{
  cout << "class_mu_1_Value:\t";
  for (int i=0; i<2; i++)
    cout << class_mu_1_Value[i];
  cout << " " << undefined_class_mu_1_Value << "\n";
}
void PermSet::Print_class_mu_1_Proc()
{
  cout << "class_mu_1_Proc:\t";
  for (int i=0; i<3; i++)
    cout << class_mu_1_Proc[i];
  cout << " " << undefined_class_mu_1_Proc << "\n";
}
bool PermSet::MoreThanOneRemain()
{
  int i,j;
  if (AlreadyOnlyOneRemain)
    return FALSE;
  else {
    for (i=0; i<2; i++)
      for (j=0; j<2; j++)
        if (i!=j && class_mu_1_Value[i]== class_mu_1_Value[j])
	    return TRUE;
    for (i=0; i<3; i++)
      for (j=0; j<3; j++)
        if (i!=j && class_mu_1_Proc[i]== class_mu_1_Proc[j])
	    return TRUE;
  }
  AlreadyOnlyOneRemain = TRUE;
  return FALSE;
}
PermSet::PermSet()
: Presentation(Simple)
{
  int i,j,k;
  if (  args->sym_alg.mode == argsym_alg::Exhaustive_Fast_Canonicalize
     || args->sym_alg.mode == argsym_alg::Heuristic_Fast_Canonicalize) {
    mu_1_Value Perm0[2];
    mu_1_Proc Perm1[3];

  /********************
   declaration of class variables
  ********************/
  in = new bool[12];
 in_mu_1_Value = new int[12];
 perm_mu_1_Value = new arr_mu_1_Value[2];
 revperm_mu_1_Value = new arr_mu_1_Value[2];
 in_mu_1_Proc = new int[12];
 perm_mu_1_Proc = new arr_mu_1_Proc[6];
 revperm_mu_1_Proc = new arr_mu_1_Proc[6];

    // Set perm and revperm
    count = 0;
    for (i=4; i<=5; i++)
      {
        Perm0[0].value(i);
        GenPerm0(Perm0, 1, count);
      }
    if (count!=2)
      Error.Error( "unable to initialize PermSet");
    for (i=0; i<2; i++)
      for (j=4; j<=5; j++)
        for (k=4; k<=5; k++)
          if (revperm_mu_1_Value[i][k-4]==j)   // k - base 
            perm_mu_1_Value[i][j-4]=k; // j - base 
    count = 0;
    for (i=1; i<=3; i++)
      {
        Perm1[0].value(i);
        GenPerm1(Perm1, 1, count);
      }
    if (count!=6)
      Error.Error( "unable to initialize PermSet");
    for (i=0; i<6; i++)
      for (j=1; j<=3; j++)
        for (k=1; k<=3; k++)
          if (revperm_mu_1_Proc[i][k-1]==j)   // k - base 
            perm_mu_1_Proc[i][j-1]=k; // j - base 

    // setting up combination of permutations
    // for different scalarset
    int carry;
    int i_mu_1_Value = 0;
    int i_mu_1_Proc = 0;
    size = 12;
    count = 12;
    for (i=0; i<12; i++)
      {
        carry = 1;
        in[i]= TRUE;
      in_mu_1_Value[i] = i_mu_1_Value;
      i_mu_1_Value += carry;
      if (i_mu_1_Value >= 2) { i_mu_1_Value = 0; carry = 1; } 
      else { carry = 0; } 
      in_mu_1_Proc[i] = i_mu_1_Proc;
      i_mu_1_Proc += carry;
      if (i_mu_1_Proc >= 6) { i_mu_1_Proc = 0; carry = 1; } 
      else { carry = 0; } 
    }
  }
  else
  {

  /********************
   declaration of class variables
  ********************/
  in = new bool[1];
 in_mu_1_Value = new int[1];
 perm_mu_1_Value = new arr_mu_1_Value[1];
 revperm_mu_1_Value = new arr_mu_1_Value[1];
 in_mu_1_Proc = new int[1];
 perm_mu_1_Proc = new arr_mu_1_Proc[1];
 revperm_mu_1_Proc = new arr_mu_1_Proc[1];
  in[0] = TRUE;
    in_mu_1_Value[0] = 0;
    in_mu_1_Proc[0] = 0;
  }
}
void PermSet::ResetToSimple()
{
  int i;
  for (i=0; i<2; i++)
    class_mu_1_Value[i]=0;
  undefined_class_mu_1_Value=0;
  OnlyOneRemain_mu_1_Value = FALSE;
  for (i=0; i<3; i++)
    class_mu_1_Proc[i]=0;
  undefined_class_mu_1_Proc=0;
  OnlyOneRemain_mu_1_Proc = FALSE;

  AlreadyOnlyOneRemain = FALSE;
  Presentation = Simple;
}
void PermSet::ResetToExplicit()
{
  for (int i=0; i<12; i++) in[i] = TRUE;
  Presentation = Explicit;
}
void PermSet::SimpleToExplicit()
{
  int i,j,k;
  int start, class_size;
  int start_mu_1_Value[2];
  int size_mu_1_Value[2];
  bool should_be_in_mu_1_Value[2];
  int start_mu_1_Proc[3];
  int size_mu_1_Proc[3];
  bool should_be_in_mu_1_Proc[6];

  // Setup range for mapping
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Value; j++) // class number
    {
      class_size = 0;
      for (k=0; k<2; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Value[k]==j)
	  class_size++;
      for (k=0; k<2; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Value[k]==j)
	  {
	    size_mu_1_Value[k] = class_size;
	    start_mu_1_Value[k] = start;
	  }
      start+=class_size;
    }
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Proc; j++) // class number
    {
      class_size = 0;
      for (k=0; k<3; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Proc[k]==j)
	  class_size++;
      for (k=0; k<3; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Proc[k]==j)
	  {
	    size_mu_1_Proc[k] = class_size;
	    start_mu_1_Proc[k] = start;
	  }
      start+=class_size;
    }

  // To be In or not to be
  for (i=0; i<2; i++) // set up
    should_be_in_mu_1_Value[i] = TRUE;
  for (i=0; i<2; i++) // to be in or not to be
    for (k=0; k<2; k++) // step through class_mu_1_pid[k]
      if (! (perm_mu_1_Value[i][k]-4 >=start_mu_1_Value[k] 
	     && perm_mu_1_Value[i][k]-4 < start_mu_1_Value[k] + size_mu_1_Value[k]) )
  	    {
	      should_be_in_mu_1_Value[i] = FALSE;
	      break;
	    }
  for (i=0; i<6; i++) // set up
    should_be_in_mu_1_Proc[i] = TRUE;
  for (i=0; i<6; i++) // to be in or not to be
    for (k=0; k<3; k++) // step through class_mu_1_pid[k]
      if (! (perm_mu_1_Proc[i][k]-1 >=start_mu_1_Proc[k] 
	     && perm_mu_1_Proc[i][k]-1 < start_mu_1_Proc[k] + size_mu_1_Proc[k]) )
  	    {
	      should_be_in_mu_1_Proc[i] = FALSE;
	      break;
	    }

  // setup explicit representation 
  // Set perm and revperm
  for (i=0; i<12; i++)
    {
      in[i] = TRUE;
      if (in[i] && !should_be_in_mu_1_Value[in_mu_1_Value[i]]) in[i] = FALSE;
      if (in[i] && !should_be_in_mu_1_Proc[in_mu_1_Proc[i]]) in[i] = FALSE;
    }
  Presentation = Explicit;
  if (args->test_parameter1.value==0) Print_in_size();
}
void PermSet::SimpleToOne()
{
  int i,j,k;
  int class_size;
  int start;


  // Setup range for mapping
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Value; j++) // class number
    {
      class_size = 0;
      for (k=0; k<2; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Value[k]==j)
	  class_size++;
      for (k=0; k<2; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Value[k]==j)
	  {
	    size_mu_1_Value[k] = class_size;
	  }
      start+=class_size;
    }
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Proc; j++) // class number
    {
      class_size = 0;
      for (k=0; k<3; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Proc[k]==j)
	  class_size++;
      for (k=0; k<3; k++) // step through class_mu_1_pid[k]
	if (class_mu_1_Proc[k]==j)
	  {
	    size_mu_1_Proc[k] = class_size;
	  }
      start+=class_size;
    }
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Value; j++) // class number
    {
      for (k=0; k<2; k++) // step through class_mu_1_pid[k]
	    if (class_mu_1_Value[k]==j)
	      revperm_mu_1_Value[0][start++] = k+4;
    }
  for (j=0; j<2; j++)
    for (k=0; k<2; k++)
      if (revperm_mu_1_Value[0][k]==j+4)
        perm_mu_1_Value[0][j]=k+4;
  start = 0;
  for (j=0; j<=undefined_class_mu_1_Proc; j++) // class number
    {
      for (k=0; k<3; k++) // step through class_mu_1_pid[k]
	    if (class_mu_1_Proc[k]==j)
	      revperm_mu_1_Proc[0][start++] = k+1;
    }
  for (j=0; j<3; j++)
    for (k=0; k<3; k++)
      if (revperm_mu_1_Proc[0][k]==j+1)
        perm_mu_1_Proc[0][j]=k+1;
  Presentation = Explicit;
}
bool PermSet::ok0(mu_1_Value* Perm, int size, mu_1_Value k)
{
  for (int i=0; i<size; i++)
    if(Perm[i].value()==k)
      return FALSE;
  return TRUE;
}
void PermSet::GenPerm0(mu_1_Value* Perm,int size, unsigned long& count)
{
  int i;
  if (size!=2)
    {
      for (i=4; i<=5; i++)
        if(ok0(Perm,size,i))
          {
            Perm[size].value(i);
            GenPerm0(Perm, size+1, count);
          }
    }
  else
    {
      for (i=4; i<=5; i++)
        revperm_mu_1_Value[count][i-4]=Perm[i-4].value();// i - base
      count++;
    }
}
bool PermSet::ok1(mu_1_Proc* Perm, int size, mu_1_Proc k)
{
  for (int i=0; i<size; i++)
    if(Perm[i].value()==k)
      return FALSE;
  return TRUE;
}
void PermSet::GenPerm1(mu_1_Proc* Perm,int size, unsigned long& count)
{
  int i;
  if (size!=3)
    {
      for (i=1; i<=3; i++)
        if(ok1(Perm,size,i))
          {
            Perm[size].value(i);
            GenPerm1(Perm, size+1, count);
          }
    }
  else
    {
      for (i=1; i<=3; i++)
        revperm_mu_1_Proc[count][i-1]=Perm[i-1].value();// i - base
      count++;
    }
}
bool PermSet::reversed_sorted_mu_1_Value(int start, int end)
{
  int i,j;

  for (i=start; i<end; i++)
    if (revperm_mu_1_Value[0][i]<revperm_mu_1_Value[0][i+1])
      return FALSE;
  return TRUE;
}
void PermSet::reverse_reversed_mu_1_Value(int start, int end)
{
  int i,j;
  int temp;

  for (i=start, j=end; i<j; i++,j--) 
    {
      temp = revperm_mu_1_Value[0][j];
      revperm_mu_1_Value[0][j] = revperm_mu_1_Value[0][i];
      revperm_mu_1_Value[0][i] = temp;
    }
}
bool PermSet::reversed_sorted_mu_1_Proc(int start, int end)
{
  int i,j;

  for (i=start; i<end; i++)
    if (revperm_mu_1_Proc[0][i]<revperm_mu_1_Proc[0][i+1])
      return FALSE;
  return TRUE;
}
void PermSet::reverse_reversed_mu_1_Proc(int start, int end)
{
  int i,j;
  int temp;

  for (i=start, j=end; i<j; i++,j--) 
    {
      temp = revperm_mu_1_Proc[0][j];
      revperm_mu_1_Proc[0][j] = revperm_mu_1_Proc[0][i];
      revperm_mu_1_Proc[0][i] = temp;
    }
}
bool PermSet::NextPermutation()
{
  bool nexted = FALSE;
  int start, end; 
  int class_size;
  int temp;
  int j,k;

  // algorithm
  // for each class
  //   if forall in the same class reverse_sorted, 
  //     { sort again; goto next class }
  //   else
  //     {
  //       nexted = TRUE;
  //       for (j from l to r)
  // 	       if (for all j+ are reversed sorted)
  // 	         {
  // 	           swap j, j+1
  // 	           sort all j+ again
  // 	           break;
  // 	         }
  //     }
  for (start = 0; start < 2; )
    {
      end = start-1+size_mu_1_Value[revperm_mu_1_Value[0][start]-4];
      if (reversed_sorted_mu_1_Value(start,end))
	       {
	  reverse_reversed_mu_1_Value(start,end);
	  start = end+1;
	}
      else
	{
	  nexted = TRUE;
	  for (j = start; j<end; j++)
	    {
	      if (reversed_sorted_mu_1_Value(j+1,end))
		{
		  for (k = end; k>j; k--)
		    {
		      if (revperm_mu_1_Value[0][j]<revperm_mu_1_Value[0][k])
			{
			  // swap j, k
			  temp = revperm_mu_1_Value[0][j];
			  revperm_mu_1_Value[0][j] = revperm_mu_1_Value[0][k];
			  revperm_mu_1_Value[0][k] = temp;
			  break;
			}
		    }
		  reverse_reversed_mu_1_Value(j+1,end);
		  break;
		}
	    }
	  break;
	}
    }
if (!nexted) {
  for (start = 0; start < 3; )
    {
      end = start-1+size_mu_1_Proc[revperm_mu_1_Proc[0][start]-1];
      if (reversed_sorted_mu_1_Proc(start,end))
	       {
	  reverse_reversed_mu_1_Proc(start,end);
	  start = end+1;
	}
      else
	{
	  nexted = TRUE;
	  for (j = start; j<end; j++)
	    {
	      if (reversed_sorted_mu_1_Proc(j+1,end))
		{
		  for (k = end; k>j; k--)
		    {
		      if (revperm_mu_1_Proc[0][j]<revperm_mu_1_Proc[0][k])
			{
			  // swap j, k
			  temp = revperm_mu_1_Proc[0][j];
			  revperm_mu_1_Proc[0][j] = revperm_mu_1_Proc[0][k];
			  revperm_mu_1_Proc[0][k] = temp;
			  break;
			}
		    }
		  reverse_reversed_mu_1_Proc(j+1,end);
		  break;
		}
	    }
	  break;
	}
    }
}
if (!nexted) return FALSE;
  for (j=0; j<2; j++)
    for (k=0; k<2; k++)
      if (revperm_mu_1_Value[0][k]==j+4)   // k - base 
	perm_mu_1_Value[0][j]=k+4; // j - base 
  for (j=0; j<3; j++)
    for (k=0; k<3; k++)
      if (revperm_mu_1_Proc[0][k]==j+1)   // k - base 
	perm_mu_1_Proc[0][j]=k+1; // j - base 
  return TRUE;
}

/********************
 Symmetry Class
 ********************/
class SymmetryClass
{
  PermSet Perm;
  bool BestInitialized;
  state BestPermutedState;

  // utilities
  void SetBestResult(int i, state* temp);
  void ResetBestResult() {BestInitialized = FALSE;};

public:
  // initializer
  SymmetryClass() : Perm(), BestInitialized(FALSE) {};
  ~SymmetryClass() {};

  void Normalize(state* s);

  void Exhaustive_Fast_Canonicalize(state *s);
  void Heuristic_Fast_Canonicalize(state *s);
  void Heuristic_Small_Mem_Canonicalize(state *s);
  void Heuristic_Fast_Normalize(state *s);

  void MultisetSort(state* s);
};


/********************
 Symmetry Class Members
 ********************/
void SymmetryClass::MultisetSort(state* s)
{
        mu_match.MultisetSort();
        mu_prevProcs.MultisetSort();
        mu_tracked.MultisetSort();
        mu_msg_imm_sent_set.MultisetSort();
        mu_prevMsg.MultisetSort();
        mu_start.MultisetSort();
        mu_cur_idx.MultisetSort();
        mu_tar.MultisetSort();
        mu_msgBufNonEmpty.MultisetSort();
        mu_gBuf.MultisetSort();
        mu_LastWrite.MultisetSort();
        mu_selc.MultisetSort();
        mu_cur_node.MultisetSort();
        mu_prevProcReq.MultisetSort();
        mu_HomeNode.MultisetSort();
        mu_MainMemory.MultisetSort();
        mu_ackBus.MultisetSort();
        mu_msgBuf.MultisetSort();
        mu_Procs.MultisetSort();
        mu_curRequsts.MultisetSort();
}
void SymmetryClass::Normalize(state* s)
{
  switch (args->sym_alg.mode) {
  case argsym_alg::Exhaustive_Fast_Canonicalize:
    Exhaustive_Fast_Canonicalize(s);
    break;
  case argsym_alg::Heuristic_Fast_Canonicalize:
    Heuristic_Fast_Canonicalize(s);
    break;
  case argsym_alg::Heuristic_Small_Mem_Canonicalize:
    Heuristic_Small_Mem_Canonicalize(s);
    break;
  case argsym_alg::Heuristic_Fast_Normalize:
    Heuristic_Fast_Normalize(s);
    break;
  default:
    Heuristic_Fast_Canonicalize(s);
  }
}

/********************
 Permute and Canonicalize function for different types
 ********************/
void mu_1_Proc::Permute(PermSet& Perm, int i)
{
  if (Perm.Presentation != PermSet::Explicit)
    Error.Error("Internal Error: Wrong Sequence of Normalization");
  if (defined())
    value(Perm.perm_mu_1_Proc[Perm.in_mu_1_Proc[i]][value()-1]); // value - base
};
void mu_1_Proc::SimpleCanonicalize(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");

  if (defined())
    if (Perm.class_mu_1_Proc[value()-1]==Perm.undefined_class_mu_1_Proc) // value - base
      {
        // it has not been mapped to any particular value
        for (i=0; i<3; i++)
          if (Perm.class_mu_1_Proc[i] == Perm.undefined_class_mu_1_Proc && i!=value()-1)
            Perm.class_mu_1_Proc[i]++;
        value(1 + Perm.undefined_class_mu_1_Proc++);
      }
    else 
      {
        value(Perm.class_mu_1_Proc[value()-1]+1);
      }
}
void mu_1_Proc::Canonicalize(PermSet& Perm)
{
  Error.Error("Calling canonicalize() for Scalarset.");
}
void mu_1_Proc::SimpleLimit(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");

  if (defined())
    if (Perm.class_mu_1_Proc[value()-1]==Perm.undefined_class_mu_1_Proc) // value - base
      {
        // it has not been mapped to any particular value
        for (i=0; i<3; i++)
          if (Perm.class_mu_1_Proc[i] == Perm.undefined_class_mu_1_Proc && i!=value()-1)
            Perm.class_mu_1_Proc[i]++;
        Perm.undefined_class_mu_1_Proc++;
      }
}
void mu_1_Proc::ArrayLimit(PermSet& Perm) {}
void mu_1_Proc::Limit(PermSet& Perm) {}
void mu_1_Proc::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset type.\n"); };
void mu_1_Value::Permute(PermSet& Perm, int i)
{
  if (Perm.Presentation != PermSet::Explicit)
    Error.Error("Internal Error: Wrong Sequence of Normalization");
  if (defined())
    value(Perm.perm_mu_1_Value[Perm.in_mu_1_Value[i]][value()-4]); // value - base
};
void mu_1_Value::SimpleCanonicalize(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");

  if (defined())
    if (Perm.class_mu_1_Value[value()-4]==Perm.undefined_class_mu_1_Value) // value - base
      {
        // it has not been mapped to any particular value
        for (i=0; i<2; i++)
          if (Perm.class_mu_1_Value[i] == Perm.undefined_class_mu_1_Value && i!=value()-4)
            Perm.class_mu_1_Value[i]++;
        value(4 + Perm.undefined_class_mu_1_Value++);
      }
    else 
      {
        value(Perm.class_mu_1_Value[value()-4]+4);
      }
}
void mu_1_Value::Canonicalize(PermSet& Perm)
{
  Error.Error("Calling canonicalize() for Scalarset.");
}
void mu_1_Value::SimpleLimit(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");

  if (defined())
    if (Perm.class_mu_1_Value[value()-4]==Perm.undefined_class_mu_1_Value) // value - base
      {
        // it has not been mapped to any particular value
        for (i=0; i<2; i++)
          if (Perm.class_mu_1_Value[i] == Perm.undefined_class_mu_1_Value && i!=value()-4)
            Perm.class_mu_1_Value[i]++;
        Perm.undefined_class_mu_1_Value++;
      }
}
void mu_1_Value::ArrayLimit(PermSet& Perm) {}
void mu_1_Value::Limit(PermSet& Perm) {}
void mu_1_Value::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset type.\n"); };
void mu_1_Home::Permute(PermSet& Perm, int i) {};
void mu_1_Home::SimpleCanonicalize(PermSet& Perm) {};
void mu_1_Home::Canonicalize(PermSet& Perm) {};
void mu_1_Home::SimpleLimit(PermSet& Perm) {};
void mu_1_Home::ArrayLimit(PermSet& Perm) {};
void mu_1_Home::Limit(PermSet& Perm) {};
void mu_1_Home::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_Node::Permute(PermSet& Perm, int i)
{
  if (Perm.Presentation != PermSet::Explicit)
    Error.Error("Internal Error: Wrong Sequence of Normalization");
  if (defined()) {
    if ( ( value() >= 1 ) && ( value() <= 3 ) )
      value(Perm.perm_mu_1_Proc[Perm.in_mu_1_Proc[i]][value()-1]+(0)); // value - base
  }
}
void mu_1_Node::SimpleCanonicalize(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");
  if (defined()) {
    if ( ( value() >= 1 ) && ( value() <= 3 ) )
      {
        if (Perm.class_mu_1_Proc[value()-1]==Perm.undefined_class_mu_1_Proc) // value - base
          {
            // it has not been mapped to any particular value
            for (i=0; i<3; i++)
              if (Perm.class_mu_1_Proc[i] == Perm.undefined_class_mu_1_Proc && i!=value()-1)
                Perm.class_mu_1_Proc[i]++;
            value(1 + Perm.undefined_class_mu_1_Proc++);
          }
        else 
          {
            value(Perm.class_mu_1_Proc[value()-1]+1);
          }
      }
  }
}
void mu_1_Node::Canonicalize(PermSet& Perm)
{
  Error.Error("Calling canonicalize() for Scalarset.");
}
void mu_1_Node::SimpleLimit(PermSet& Perm)
{
  int i, class_number;
  if (Perm.Presentation != PermSet::Simple)
    Error.Error("Internal Error: Wrong Sequence of Normalization");
  if (defined()) {
    if ( ( value() >= 1 ) && ( value() <= 3 ) )
      if (Perm.class_mu_1_Proc[value()-1]==Perm.undefined_class_mu_1_Proc) // value - base
        {
          // it has not been mapped to any particular value
          for (i=0; i<3; i++)
            if (Perm.class_mu_1_Proc[i] == Perm.undefined_class_mu_1_Proc && i!=value()-1)
              Perm.class_mu_1_Proc[i]++;
          Perm.undefined_class_mu_1_Proc++;
        }
  }
}
void mu_1_Node::ArrayLimit(PermSet& Perm) {}
void mu_1_Node::Limit(PermSet& Perm) {}
void mu_1_Node::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for union type.\n"); };
void mu_1__type_0::Permute(PermSet& Perm, int i) {};
void mu_1__type_0::SimpleCanonicalize(PermSet& Perm) {};
void mu_1__type_0::Canonicalize(PermSet& Perm) {};
void mu_1__type_0::SimpleLimit(PermSet& Perm) {};
void mu_1__type_0::ArrayLimit(PermSet& Perm) {};
void mu_1__type_0::Limit(PermSet& Perm) {};
void mu_1__type_0::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_CurReq::Permute(PermSet& Perm, int i)
{
  mu_val.Permute(Perm,i);
};
void mu_1_CurReq::SimpleCanonicalize(PermSet& Perm)
{
  mu_val.SimpleCanonicalize(Perm);
};
void mu_1_CurReq::Canonicalize(PermSet& Perm)
{
};
void mu_1_CurReq::SimpleLimit(PermSet& Perm)
{
  mu_val.SimpleLimit(Perm);
};
void mu_1_CurReq::ArrayLimit(PermSet& Perm){}
void mu_1_CurReq::Limit(PermSet& Perm)
{
};
void mu_1_CurReq::MultisetLimit(PermSet& Perm)
{
};
void mu_1_MessageType::Permute(PermSet& Perm, int i) {};
void mu_1_MessageType::SimpleCanonicalize(PermSet& Perm) {};
void mu_1_MessageType::Canonicalize(PermSet& Perm) {};
void mu_1_MessageType::SimpleLimit(PermSet& Perm) {};
void mu_1_MessageType::ArrayLimit(PermSet& Perm) {};
void mu_1_MessageType::Limit(PermSet& Perm) {};
void mu_1_MessageType::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_Message::Permute(PermSet& Perm, int i)
{
  mu_src.Permute(Perm,i);
  mu_dst.Permute(Perm,i);
  mu_val.Permute(Perm,i);
};
void mu_1_Message::SimpleCanonicalize(PermSet& Perm)
{
  mu_src.SimpleCanonicalize(Perm);
  mu_dst.SimpleCanonicalize(Perm);
  mu_val.SimpleCanonicalize(Perm);
};
void mu_1_Message::Canonicalize(PermSet& Perm)
{
};
void mu_1_Message::SimpleLimit(PermSet& Perm)
{
  mu_src.SimpleLimit(Perm);
  mu_dst.SimpleLimit(Perm);
  mu_val.SimpleLimit(Perm);
};
void mu_1_Message::ArrayLimit(PermSet& Perm){}
void mu_1_Message::Limit(PermSet& Perm)
{
};
void mu_1_Message::MultisetLimit(PermSet& Perm)
{
};
void mu_1_HomeStateEnum::Permute(PermSet& Perm, int i) {};
void mu_1_HomeStateEnum::SimpleCanonicalize(PermSet& Perm) {};
void mu_1_HomeStateEnum::Canonicalize(PermSet& Perm) {};
void mu_1_HomeStateEnum::SimpleLimit(PermSet& Perm) {};
void mu_1_HomeStateEnum::ArrayLimit(PermSet& Perm) {};
void mu_1_HomeStateEnum::Limit(PermSet& Perm) {};
void mu_1_HomeStateEnum::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_HomeState::Permute(PermSet& Perm, int i)
{
  mu_val.Permute(Perm,i);
};
void mu_1_HomeState::SimpleCanonicalize(PermSet& Perm)
{
  mu_val.SimpleCanonicalize(Perm);
};
void mu_1_HomeState::Canonicalize(PermSet& Perm)
{
};
void mu_1_HomeState::SimpleLimit(PermSet& Perm)
{
  mu_val.SimpleLimit(Perm);
};
void mu_1_HomeState::ArrayLimit(PermSet& Perm){}
void mu_1_HomeState::Limit(PermSet& Perm)
{
};
void mu_1_HomeState::MultisetLimit(PermSet& Perm)
{
};
void mu_1_ProcStateEnum::Permute(PermSet& Perm, int i) {};
void mu_1_ProcStateEnum::SimpleCanonicalize(PermSet& Perm) {};
void mu_1_ProcStateEnum::Canonicalize(PermSet& Perm) {};
void mu_1_ProcStateEnum::SimpleLimit(PermSet& Perm) {};
void mu_1_ProcStateEnum::ArrayLimit(PermSet& Perm) {};
void mu_1_ProcStateEnum::Limit(PermSet& Perm) {};
void mu_1_ProcStateEnum::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_ProcState::Permute(PermSet& Perm, int i)
{
  mu_val.Permute(Perm,i);
};
void mu_1_ProcState::SimpleCanonicalize(PermSet& Perm)
{
  mu_val.SimpleCanonicalize(Perm);
};
void mu_1_ProcState::Canonicalize(PermSet& Perm)
{
};
void mu_1_ProcState::SimpleLimit(PermSet& Perm)
{
  mu_val.SimpleLimit(Perm);
};
void mu_1_ProcState::ArrayLimit(PermSet& Perm){}
void mu_1_ProcState::Limit(PermSet& Perm)
{
};
void mu_1_ProcState::MultisetLimit(PermSet& Perm)
{
};
void mu_1__type_1::Permute(PermSet& Perm, int i) {};
void mu_1__type_1::SimpleCanonicalize(PermSet& Perm) {};
void mu_1__type_1::Canonicalize(PermSet& Perm) {};
void mu_1__type_1::SimpleLimit(PermSet& Perm) {};
void mu_1__type_1::ArrayLimit(PermSet& Perm) {};
void mu_1__type_1::Limit(PermSet& Perm) {};
void mu_1__type_1::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for enum type.\n"); };
void mu_1_CoreReq::Permute(PermSet& Perm, int i)
{
  mu_cl.Permute(Perm,i);
};
void mu_1_CoreReq::SimpleCanonicalize(PermSet& Perm)
{
  mu_cl.SimpleCanonicalize(Perm);
};
void mu_1_CoreReq::Canonicalize(PermSet& Perm)
{
};
void mu_1_CoreReq::SimpleLimit(PermSet& Perm)
{
  mu_cl.SimpleLimit(Perm);
};
void mu_1_CoreReq::ArrayLimit(PermSet& Perm){}
void mu_1_CoreReq::Limit(PermSet& Perm)
{
};
void mu_1_CoreReq::MultisetLimit(PermSet& Perm)
{
};
void mu_1__type_2::Permute(PermSet& Perm, int i)
{
  static mu_1__type_2 temp("Permute_mu_1__type_2",-1);
  int j;
  for (j=0; j<3; j++)
    array[j].Permute(Perm, i);
};
void mu_1__type_2::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_2::Canonicalize(PermSet& Perm){};
void mu_1__type_2::SimpleLimit(PermSet& Perm){}
void mu_1__type_2::ArrayLimit(PermSet& Perm) {}
void mu_1__type_2::Limit(PermSet& Perm){}
void mu_1__type_2::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };
void mu_1__type_3::Permute(PermSet& Perm, int i) {};
void mu_1__type_3::SimpleCanonicalize(PermSet& Perm) {};
void mu_1__type_3::Canonicalize(PermSet& Perm) {};
void mu_1__type_3::SimpleLimit(PermSet& Perm) {};
void mu_1__type_3::ArrayLimit(PermSet& Perm) {};
void mu_1__type_3::Limit(PermSet& Perm) {};
void mu_1__type_3::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for subrange type.\n"); };
void mu__subrange_19::Permute(PermSet& Perm, int i) {};
void mu__subrange_19::SimpleCanonicalize(PermSet& Perm) {};
void mu__subrange_19::Canonicalize(PermSet& Perm) {};
void mu__subrange_19::SimpleLimit(PermSet& Perm) {};
void mu__subrange_19::ArrayLimit(PermSet& Perm) {};
void mu__subrange_19::Limit(PermSet& Perm) {};
void mu__subrange_19::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for subrange type.\n"); };
void mu_1__type_4::Permute(PermSet& Perm, int i)
{
  static mu_1__type_4 temp("Permute_mu_1__type_4",-1);
  int j;
  for (j=0; j<1; j++)
    array[j].Permute(Perm, i);
};
void mu_1__type_4::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_4::Canonicalize(PermSet& Perm){};
void mu_1__type_4::SimpleLimit(PermSet& Perm){}
void mu_1__type_4::ArrayLimit(PermSet& Perm) {}
void mu_1__type_4::Limit(PermSet& Perm){}
void mu_1__type_4::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };
void mu_1__type_5::Permute(PermSet& Perm, int i) {};
void mu_1__type_5::SimpleCanonicalize(PermSet& Perm) {};
void mu_1__type_5::Canonicalize(PermSet& Perm) {};
void mu_1__type_5::SimpleLimit(PermSet& Perm) {};
void mu_1__type_5::ArrayLimit(PermSet& Perm) {};
void mu_1__type_5::Limit(PermSet& Perm) {};
void mu_1__type_5::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for subrange type.\n"); };
void mu_1__type_6::Permute(PermSet& Perm, int i)
{
  static mu_1__type_6 temp("Permute_mu_1__type_6",-1);
  int j;
  for (j=0; j<3; j++)
    array[j].Permute(Perm, i);
  temp = *this;
  for (j=1; j<=3; j++)
    (*this)[j] = temp[Perm.revperm_mu_1_Proc[Perm.in_mu_1_Proc[i]][j-1]];};
void mu_1__type_6::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_6::Canonicalize(PermSet& Perm){};
void mu_1__type_6::SimpleLimit(PermSet& Perm){}
void mu_1__type_6::ArrayLimit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // sorting
  int count_mu_1_Proc;
  int compare;
  static mu_1_ProcState value[3];
  // limit
  bool exists;
  bool split;
  bool goodset_mu_1_Proc[3];
  bool pos_mu_1_Proc[3][3];
  // sorting mu_1_Proc
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          pos_mu_1_Proc[i][j]=FALSE;
      count_mu_1_Proc = 0;
      for (i=0; i<3; i++)
        {
          for (j=0; j<count_mu_1_Proc; j++)
            {
              compare = CompareWeight(value[j],(*this)[i+1]);
              if (compare==0)
                {
                  pos_mu_1_Proc[j][i]= TRUE;
                  break;
                }
              else if (compare>0)
                {
                  for (k=count_mu_1_Proc; k>j; k--)
                    {
                      value[k] = value[k-1];
                      for (z=0; z<3; z++)
                        pos_mu_1_Proc[k][z] = pos_mu_1_Proc[k-1][z];
                    }
                  value[j] = (*this)[i+1];
                  for (z=0; z<3; z++)
                    pos_mu_1_Proc[j][z] = FALSE;
                  pos_mu_1_Proc[j][i] = TRUE;
                  count_mu_1_Proc++;
                  break;
                }
            }
          if (j==count_mu_1_Proc)
            {
              value[j] = (*this)[i+1];
              for (z=0; z<3; z++)
                pos_mu_1_Proc[j][z] = FALSE;
              pos_mu_1_Proc[j][i] = TRUE;
              count_mu_1_Proc++;
            }
        }
    }
  // if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc>1)
    {
      // limit
      for (j=0; j<3; j++) // class priority
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] && Perm.class_mu_1_Proc[k] == j)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                    pos_mu_1_Proc[i][k] = FALSE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) 
                      split= TRUE;
                  if (split)
                    {
                      for (k=0; k<3; k++)
                        if (Perm.class_mu_1_Proc[k]>j
                            || ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) )
                          Perm.class_mu_1_Proc[k]++;
                      Perm.undefined_class_mu_1_Proc++;
                    }
                }
            }
        }
    }
}
void mu_1__type_6::Limit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // while guard
  bool while_guard, while_guard_temp;
  // sorting
  static mu_1_ProcState value[3];
  // limit
  bool exists;
  bool split;
  int i0;
  int count_mu_1_Proc, oldcount_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  int count_mu_1_Value, oldcount_mu_1_Value;
  bool pos_mu_1_Value[2][2];
  bool goodset_mu_1_Value[2];
  // count_ corresponds to the number of equivalence class within the
  // scalarset value.  If count_ == size of the scalarset, then a unique
  // permutation has been found.

  // pos_ is a relation on a equivalence class number and a scalarset value.

  // initializing pos array
  for (i=0; i<3; i++)
    for (j=0; j<3; j++)
      pos_mu_1_Proc[i][j]=FALSE;
  count_mu_1_Proc = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<3; i++)
       if (Perm.class_mu_1_Proc[i] == count_mu_1_Proc)
         {
           pos_mu_1_Proc[count_mu_1_Proc][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Proc++;
      else break;
    }
  // count_ corresponds to the number of equivalence class within the
  // scalarset value.  If count_ == size of the scalarset, then a unique
  // permutation has been found.

  // pos_ is a relation on a equivalence class number and a scalarset value.

  // initializing pos array
  for (i=0; i<2; i++)
    for (j=0; j<2; j++)
      pos_mu_1_Value[i][j]=FALSE;
  count_mu_1_Value = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<2; i++)
       if (Perm.class_mu_1_Value[i] == count_mu_1_Value)
         {
           pos_mu_1_Value[count_mu_1_Value][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Value++;
      else break;
    }

  // refinement -- checking priority in general
  while_guard = FALSE;
  while_guard = while_guard || (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3);
  while_guard = while_guard || (Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2);
  while ( while_guard )
    {
      oldcount_mu_1_Proc = count_mu_1_Proc;
      oldcount_mu_1_Value = count_mu_1_Value;

      // refinement -- graph structure for two scalarsets
      //               as in array S1 of S2
      // only if there is more than 1 permutation in class
      if ( (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
           || ( Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2) )
        {
          exists = FALSE;
          split = FALSE;
          for (k=0; k<3; k++) // step through class
            if ((*this)[k+1].mu_val.isundefined())
              exists = TRUE;
            else
              split = TRUE;
          if (exists && split)
            {
              for (i=0; i<count_mu_1_Proc; i++) // scan through array index priority
                for (j=0; j<count_mu_1_Value; j++) //scan through element priority
                  {
                    exists = FALSE;
                    for (k=0; k<3; k++) // initialize goodset
                      goodset_mu_1_Proc[k] = FALSE;
                    for (k=0; k<2; k++) // initialize goodset
                      goodset_mu_1_Value[k] = FALSE;
                    for (k=0; k<3; k++) // scan array index
                      // set goodsets
                      if (pos_mu_1_Proc[i][k] 
                          && !(*this)[k+1].mu_val.isundefined()
                          && pos_mu_1_Value[j][(*this)[k+1].mu_val-4])
                        {
                          exists = TRUE;
                          goodset_mu_1_Proc[k] = TRUE;
                          goodset_mu_1_Value[(*this)[k+1].mu_val-4] = TRUE;
                        }
                    if (exists)
                      {
                        // set split for the array index type
                        split=FALSE;
                        for (k=0; k<3; k++)
                          if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Proc; z>i; z--)
                              for (k=0; k<3; k++)
                                pos_mu_1_Proc[z][k] = pos_mu_1_Proc[z-1][k];
                            // split pos
                            for (k=0; k<3; k++)
                              {
                                if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i][k] = FALSE;
                                if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i+1][k] = FALSE;
                              }
                            count_mu_1_Proc++;
                          }
                        // set split for the element type
                        split=FALSE;
                        for (k=0; k<2; k++)
                          if ( pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Value; z>j; z--)
                              for (k=0; k<2; k++)
                                pos_mu_1_Value[z][k] = pos_mu_1_Value[z-1][k];
                            // split pos
                            for (k=0; k<2; k++)
                              {
                                if (pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j][k] = FALSE;
                                if (pos_mu_1_Value[j+1][k] && goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j+1][k] = FALSE;
                              }
                            count_mu_1_Value++;
                          }
                      }
                  }
            }
        }
      while_guard = FALSE;
      while_guard = while_guard || (oldcount_mu_1_Proc!=count_mu_1_Proc);
      while_guard = while_guard || (oldcount_mu_1_Value!=count_mu_1_Value);
      while_guard_temp = while_guard;
      while_guard = FALSE;
      while_guard = while_guard || count_mu_1_Proc<3;
      while_guard = while_guard || count_mu_1_Value<2;
      while_guard = while_guard && while_guard_temp;
    } // end while
  // enter the result into class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          if (pos_mu_1_Proc[i][j])
            Perm.class_mu_1_Proc[j] = i;
      Perm.undefined_class_mu_1_Proc=0;
      for (j=0; j<3; j++)
        if (Perm.class_mu_1_Proc[j]>Perm.undefined_class_mu_1_Proc)
          Perm.undefined_class_mu_1_Proc=Perm.class_mu_1_Proc[j];
    }
  // enter the result into class
  if (Perm.MTO_class_mu_1_Value())
    {
      for (i=0; i<2; i++)
        for (j=0; j<2; j++)
          if (pos_mu_1_Value[i][j])
            Perm.class_mu_1_Value[j] = i;
      Perm.undefined_class_mu_1_Value=0;
      for (j=0; j<2; j++)
        if (Perm.class_mu_1_Value[j]>Perm.undefined_class_mu_1_Value)
          Perm.undefined_class_mu_1_Value=Perm.class_mu_1_Value[j];
    }
}
void mu_1__type_6::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };
void mu_1__type_7::Permute(PermSet& Perm, int i)
{
  static mu_1__type_7 temp("Permute_mu_1__type_7",-1);
  int j;
  for (j=0; j<4; j++)
    array[j].Permute(Perm, i);
  temp = *this;
  for (j=1; j<=3; j++)
      (*this)[j].value(temp[Perm.revperm_mu_1_Proc[Perm.in_mu_1_Proc[i]][j-1]].value());
};
void mu_1__type_7::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_7::Canonicalize(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // sorting
  static mu_0_boolean value[4];
  int compare;
  // limit
  bool exists;
  bool split;
  // range mapping
  int start;
  int class_size;
  // canonicalization
  static mu_1__type_7 temp;
  int count_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  int size_mu_1_Proc[3];
  int start_mu_1_Proc[3];
  // sorting mu_1_Proc
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          pos_mu_1_Proc[i][j]=FALSE;
      count_mu_1_Proc = 0;
      for (i=0; i<3; i++)
        {
          for (j=0; j<count_mu_1_Proc; j++)
            {
              compare = CompareWeight(value[j],(*this)[i+1]);
              if (compare==0)
                {
                  pos_mu_1_Proc[j][i]= TRUE;
                  break;
                }
              else if (compare>0)
                {
                  for (k=count_mu_1_Proc; k>j; k--)
                    {
                      value[k].value(value[k-1].value());
                      for (z=0; z<3; z++)
                        pos_mu_1_Proc[k][z] = pos_mu_1_Proc[k-1][z];
                    }
                  value[j].value((*this)[i+1].value());
                  for (z=0; z<3; z++)
                    pos_mu_1_Proc[j][z] = FALSE;
                  pos_mu_1_Proc[j][i] = TRUE;
                  count_mu_1_Proc++;
                  break;
                }
            }
          if (j==count_mu_1_Proc)
            {
                value[j].value((*this)[i+1].value());
              for (z=0; z<3; z++)
                pos_mu_1_Proc[j][z] = FALSE;
              pos_mu_1_Proc[j][i] = TRUE;
              count_mu_1_Proc++;
            }
        }
    }
  // if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc>1)
    {
      // limit
      for (j=0; j<3; j++) // class priority
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] && Perm.class_mu_1_Proc[k] == j)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                    pos_mu_1_Proc[i][k] = FALSE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) 
                      split= TRUE;
                  if (split)
                    {
                      for (k=0; k<3; k++)
                        if (Perm.class_mu_1_Proc[k]>j
                            || ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) )
                          Perm.class_mu_1_Proc[k]++;
                      Perm.undefined_class_mu_1_Proc++;
                    }
                }
            }
        }
    }
  if (Perm.MTO_class_mu_1_Proc())
    {

      // setup range for maping
      start = 0;
      for (j=0; j<=Perm.undefined_class_mu_1_Proc; j++) // class number
        {
          class_size = 0;
          for (k=0; k<3; k++) // step through class[k]
            if (Perm.class_mu_1_Proc[k]==j)
              class_size++;
          for (k=0; k<3; k++) // step through class[k]
            if (Perm.class_mu_1_Proc[k]==j)
              {
                size_mu_1_Proc[k] = class_size;
                start_mu_1_Proc[k] = start;
              }
          start+=class_size;
        }

      // canonicalize
      temp = *this;
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
         if (i >=start_mu_1_Proc[j] 
             && i < start_mu_1_Proc[j] + size_mu_1_Proc[j])
           {
             array[i+1].value(temp[j+1].value());
             break;
           }
    }
  else
    {

      // fast canonicalize
      temp = *this;
      for (j=0; j<3; j++)
        array[Perm.class_mu_1_Proc[j]+1].value(temp[j+1].value());
    }
}
void mu_1__type_7::SimpleLimit(PermSet& Perm){}
void mu_1__type_7::ArrayLimit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // sorting
  int compare;
  static mu_0_boolean value[4];
  // limit
  bool exists;
  bool split;
  int count_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  // sorting mu_1_Proc
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          pos_mu_1_Proc[i][j]=FALSE;
      count_mu_1_Proc = 0;
      for (i=0; i<3; i++)
        {
          for (j=0; j<count_mu_1_Proc; j++)
            {
              compare = CompareWeight(value[j],(*this)[i+1]);
              if (compare==0)
                {
                  pos_mu_1_Proc[j][i]= TRUE;
                  break;
                }
              else if (compare>0)
                {
                  for (k=count_mu_1_Proc; k>j; k--)
                    {
                      value[k].value(value[k-1].value());
                      for (z=0; z<3; z++)
                        pos_mu_1_Proc[k][z] = pos_mu_1_Proc[k-1][z];
                    }
                  value[j].value((*this)[i+1].value());
                  for (z=0; z<3; z++)
                    pos_mu_1_Proc[j][z] = FALSE;
                  pos_mu_1_Proc[j][i] = TRUE;
                  count_mu_1_Proc++;
                  break;
                }
            }
          if (j==count_mu_1_Proc)
            {
                value[j].value((*this)[i+1].value());
              for (z=0; z<3; z++)
                pos_mu_1_Proc[j][z] = FALSE;
              pos_mu_1_Proc[j][i] = TRUE;
              count_mu_1_Proc++;
            }
        }
    }
  // if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc>1)
    {
      // limit
      for (j=0; j<3; j++) // class priority
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] && Perm.class_mu_1_Proc[k] == j)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                    pos_mu_1_Proc[i][k] = FALSE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) 
                      split= TRUE;
                  if (split)
                    {
                      for (k=0; k<3; k++)
                        if (Perm.class_mu_1_Proc[k]>j
                            || ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) )
                          Perm.class_mu_1_Proc[k]++;
                      Perm.undefined_class_mu_1_Proc++;
                    }
                }
            }
        }
    }
}
void mu_1__type_7::Limit(PermSet& Perm){}
void mu_1__type_7::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };
void mu_1__type_8::Permute(PermSet& Perm, int i)
{
  static mu_1__type_8 temp("Permute_mu_1__type_8",-1);
  int j;
  for (j=0; j<4; j++)
    array[j].Permute(Perm, i);
  temp = *this;
  for (j=1; j<=3; j++)
    (*this)[j] = temp[Perm.revperm_mu_1_Proc[Perm.in_mu_1_Proc[i]][j-1]];
};
void mu_1__type_8::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_8::Canonicalize(PermSet& Perm){};
void mu_1__type_8::SimpleLimit(PermSet& Perm){}
void mu_1__type_8::ArrayLimit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // sorting
  int compare;
  static mu_1_Message value[4];
  // limit
  bool exists;
  bool split;
  int count_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  // sorting mu_1_Proc
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          pos_mu_1_Proc[i][j]=FALSE;
      count_mu_1_Proc = 0;
      for (i=0; i<3; i++)
        {
          for (j=0; j<count_mu_1_Proc; j++)
            {
              compare = CompareWeight(value[j],(*this)[i+1]);
              if (compare==0)
                {
                  pos_mu_1_Proc[j][i]= TRUE;
                  break;
                }
              else if (compare>0)
                {
                  for (k=count_mu_1_Proc; k>j; k--)
                    {
                      value[k] = value[k-1];
                      for (z=0; z<3; z++)
                        pos_mu_1_Proc[k][z] = pos_mu_1_Proc[k-1][z];
                    }
                  value[j] = (*this)[i+1];
                  for (z=0; z<3; z++)
                    pos_mu_1_Proc[j][z] = FALSE;
                  pos_mu_1_Proc[j][i] = TRUE;
                  count_mu_1_Proc++;
                  break;
                }
            }
          if (j==count_mu_1_Proc)
            {
              value[j] = (*this)[i+1];
              for (z=0; z<3; z++)
                pos_mu_1_Proc[j][z] = FALSE;
              pos_mu_1_Proc[j][i] = TRUE;
              count_mu_1_Proc++;
            }
        }
    }
  // if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc>1)
    {
      // limit
      for (j=0; j<3; j++) // class priority
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] && Perm.class_mu_1_Proc[k] == j)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                    pos_mu_1_Proc[i][k] = FALSE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) 
                      split= TRUE;
                  if (split)
                    {
                      for (k=0; k<3; k++)
                        if (Perm.class_mu_1_Proc[k]>j
                            || ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) )
                          Perm.class_mu_1_Proc[k]++;
                      Perm.undefined_class_mu_1_Proc++;
                    }
                }
            }
        }
    }
}
void mu_1__type_8::Limit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // while guard
  bool while_guard, while_guard_temp;
  // sorting
  static mu_1_Message value[4];
  // limit
  bool exists;
  bool split;
  int i0;
  int count_mu_1_Value, oldcount_mu_1_Value;
  bool pos_mu_1_Value[2][2];
  bool goodset_mu_1_Value[2];
  int count_mu_1_Proc, oldcount_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  // initializing pos array
  for (i=0; i<2; i++)
    for (j=0; j<2; j++)
      pos_mu_1_Value[i][j]=FALSE;
  count_mu_1_Value = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<2; i++)
       if (Perm.class_mu_1_Value[i] == count_mu_1_Value)
         {
           pos_mu_1_Value[count_mu_1_Value][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Value++;
      else break;
    }
  // initializing pos array
  for (i=0; i<3; i++)
    for (j=0; j<3; j++)
      pos_mu_1_Proc[i][j]=FALSE;
  count_mu_1_Proc = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<3; i++)
       if (Perm.class_mu_1_Proc[i] == count_mu_1_Proc)
         {
           pos_mu_1_Proc[count_mu_1_Proc][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Proc++;
      else break;
    }

  // refinement -- check selfloop
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
    {
      exists = FALSE;
      split = FALSE;
      // if there exists both self loop and non-self loop
      for (k=0; k<3; k++) // step through class
        if ((*this)[k+1].mu_src.isundefined()
            ||(*this)[k+1].mu_src!=k+1)
          exists = TRUE;
        else
          split = TRUE;
      if (exists && split)
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] 
                    && !(*this)[k+1].mu_src.isundefined()
                    && (*this)[k+1].mu_src==k+1)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] ) 
                          split= TRUE;
                  if (split)
                    {
                      for (j=count_mu_1_Proc; j>i; j--)
                        for (k=0; k<3; k++)
                          pos_mu_1_Proc[j][k] = pos_mu_1_Proc[j-1][k];
                      for (k=0; k<3; k++)
                        {
                          if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                            pos_mu_1_Proc[i][k] = FALSE;
                          if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                            pos_mu_1_Proc[i+1][k] = FALSE;
                        }
                      count_mu_1_Proc++; i++;
                    }
                }
            }
        }
    }

  // refinement -- check selfloop
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
    {
      exists = FALSE;
      split = FALSE;
      // if there exists both self loop and non-self loop
      for (k=0; k<3; k++) // step through class
        if ((*this)[k+1].mu_dst.isundefined()
            ||(*this)[k+1].mu_dst!=k+1)
          exists = TRUE;
        else
          split = TRUE;
      if (exists && split)
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] 
                    && !(*this)[k+1].mu_dst.isundefined()
                    && (*this)[k+1].mu_dst==k+1)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] ) 
                          split= TRUE;
                  if (split)
                    {
                      for (j=count_mu_1_Proc; j>i; j--)
                        for (k=0; k<3; k++)
                          pos_mu_1_Proc[j][k] = pos_mu_1_Proc[j-1][k];
                      for (k=0; k<3; k++)
                        {
                          if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                            pos_mu_1_Proc[i][k] = FALSE;
                          if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                            pos_mu_1_Proc[i+1][k] = FALSE;
                        }
                      count_mu_1_Proc++; i++;
                    }
                }
            }
        }
    }

  // refinement -- checking priority in general
  while_guard = FALSE;
  while_guard = while_guard || (Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2);
  while_guard = while_guard || (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3);
  while ( while_guard )
    {
      oldcount_mu_1_Value = count_mu_1_Value;
      oldcount_mu_1_Proc = count_mu_1_Proc;

      // refinement -- graph structure for a single scalarset
      //               as in array S1 of S1
      // only if there is more than 1 permutation in class
      if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
        {
          exists = FALSE;
          split = FALSE;
          for (k=0; k<3; k++) // step through class
            if (!(*this)[k+1].mu_src.isundefined()
                &&(*this)[k+1].mu_src!=k+1
                &&(*this)[k+1].mu_src>=1
                &&(*this)[k+1].mu_src<=3)
              exists = TRUE;
          if (exists)
            {
              for (i=0; i<count_mu_1_Proc; i++) // for value priority
                {
                  for (j=0; j<count_mu_1_Proc; j++) // for value priority
                    {
                      exists = FALSE;
                      for (k=0; k<3; k++) // step through class
                        goodset_mu_1_Proc[k] = FALSE;
                      for (k=0; k<3; k++) // step through class
                        if (pos_mu_1_Proc[i][k] 
                            && !(*this)[k+1].mu_src.isundefined()
                            && (*this)[k+1].mu_src!=k+1
                            && (*this)[k+1].mu_src>=1
                            && (*this)[k+1].mu_src<=3
                            && pos_mu_1_Proc[j][(*this)[k+1].mu_src-1])
                          {
                            exists = TRUE;
                            goodset_mu_1_Proc[k] = TRUE;
                          }
                      if (exists)
                        {
                          split=FALSE;
                          for (k=0; k<3; k++)
                            if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] ) 
                              split= TRUE;
                          if (split)
                            {
                              for (j=count_mu_1_Proc; j>i; j--)
                                for (k=0; k<3; k++)
                                  pos_mu_1_Proc[j][k] = pos_mu_1_Proc[j-1][k];
                              for (k=0; k<3; k++)
                                {
                                  if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                                    pos_mu_1_Proc[i][k] = FALSE;
                                  if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                                    pos_mu_1_Proc[i+1][k] = FALSE;                  
                                }
                              count_mu_1_Proc++;
                            }
                        }
                    }
                }
            }
        }

      // refinement -- graph structure for a single scalarset
      //               as in array S1 of S1
      // only if there is more than 1 permutation in class
      if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
        {
          exists = FALSE;
          split = FALSE;
          for (k=0; k<3; k++) // step through class
            if (!(*this)[k+1].mu_dst.isundefined()
                &&(*this)[k+1].mu_dst!=k+1
                &&(*this)[k+1].mu_dst>=1
                &&(*this)[k+1].mu_dst<=3)
              exists = TRUE;
          if (exists)
            {
              for (i=0; i<count_mu_1_Proc; i++) // for value priority
                {
                  for (j=0; j<count_mu_1_Proc; j++) // for value priority
                    {
                      exists = FALSE;
                      for (k=0; k<3; k++) // step through class
                        goodset_mu_1_Proc[k] = FALSE;
                      for (k=0; k<3; k++) // step through class
                        if (pos_mu_1_Proc[i][k] 
                            && !(*this)[k+1].mu_dst.isundefined()
                            && (*this)[k+1].mu_dst!=k+1
                            && (*this)[k+1].mu_dst>=1
                            && (*this)[k+1].mu_dst<=3
                            && pos_mu_1_Proc[j][(*this)[k+1].mu_dst-1])
                          {
                            exists = TRUE;
                            goodset_mu_1_Proc[k] = TRUE;
                          }
                      if (exists)
                        {
                          split=FALSE;
                          for (k=0; k<3; k++)
                            if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] ) 
                              split= TRUE;
                          if (split)
                            {
                              for (j=count_mu_1_Proc; j>i; j--)
                                for (k=0; k<3; k++)
                                  pos_mu_1_Proc[j][k] = pos_mu_1_Proc[j-1][k];
                              for (k=0; k<3; k++)
                                {
                                  if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                                    pos_mu_1_Proc[i][k] = FALSE;
                                  if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                                    pos_mu_1_Proc[i+1][k] = FALSE;                  
                                }
                              count_mu_1_Proc++;
                            }
                        }
                    }
                }
            }
        }

      // refinement -- graph structure for two scalarsets
      //               as in array S1 of S2
      // only if there is more than 1 permutation in class
      if ( (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
           || ( Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2) )
        {
          exists = FALSE;
          split = FALSE;
          for (k=0; k<3; k++) // step through class
            if ((*this)[k+1].mu_val.isundefined())
              exists = TRUE;
            else
              split = TRUE;
          if (exists && split)
            {
              for (i=0; i<count_mu_1_Proc; i++) // scan through array index priority
                for (j=0; j<count_mu_1_Value; j++) //scan through element priority
                  {
                    exists = FALSE;
                    for (k=0; k<3; k++) // initialize goodset
                      goodset_mu_1_Proc[k] = FALSE;
                    for (k=0; k<2; k++) // initialize goodset
                      goodset_mu_1_Value[k] = FALSE;
                    for (k=0; k<3; k++) // scan array index
                      // set goodsets
                      if (pos_mu_1_Proc[i][k] 
                          && !(*this)[k+1].mu_val.isundefined()
                          && pos_mu_1_Value[j][(*this)[k+1].mu_val-4])
                        {
                          exists = TRUE;
                          goodset_mu_1_Proc[k] = TRUE;
                          goodset_mu_1_Value[(*this)[k+1].mu_val-4] = TRUE;
                        }
                    if (exists)
                      {
                        // set split for the array index type
                        split=FALSE;
                        for (k=0; k<3; k++)
                          if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Proc; z>i; z--)
                              for (k=0; k<3; k++)
                                pos_mu_1_Proc[z][k] = pos_mu_1_Proc[z-1][k];
                            // split pos
                            for (k=0; k<3; k++)
                              {
                                if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i][k] = FALSE;
                                if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i+1][k] = FALSE;
                              }
                            count_mu_1_Proc++;
                          }
                        // set split for the element type
                        split=FALSE;
                        for (k=0; k<2; k++)
                          if ( pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Value; z>j; z--)
                              for (k=0; k<2; k++)
                                pos_mu_1_Value[z][k] = pos_mu_1_Value[z-1][k];
                            // split pos
                            for (k=0; k<2; k++)
                              {
                                if (pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j][k] = FALSE;
                                if (pos_mu_1_Value[j+1][k] && goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j+1][k] = FALSE;
                              }
                            count_mu_1_Value++;
                          }
                      }
                  }
            }
        }
      while_guard = FALSE;
      while_guard = while_guard || (oldcount_mu_1_Value!=count_mu_1_Value);
      while_guard = while_guard || (oldcount_mu_1_Proc!=count_mu_1_Proc);
      while_guard_temp = while_guard;
      while_guard = FALSE;
      while_guard = while_guard || count_mu_1_Value<2;
      while_guard = while_guard || count_mu_1_Proc<3;
      while_guard = while_guard && while_guard_temp;
    } // end while
  // enter the result into class
  if (Perm.MTO_class_mu_1_Value())
    {
      for (i=0; i<2; i++)
        for (j=0; j<2; j++)
          if (pos_mu_1_Value[i][j])
            Perm.class_mu_1_Value[j] = i;
      Perm.undefined_class_mu_1_Value=0;
      for (j=0; j<2; j++)
        if (Perm.class_mu_1_Value[j]>Perm.undefined_class_mu_1_Value)
          Perm.undefined_class_mu_1_Value=Perm.class_mu_1_Value[j];
    }
  // enter the result into class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          if (pos_mu_1_Proc[i][j])
            Perm.class_mu_1_Proc[j] = i;
      Perm.undefined_class_mu_1_Proc=0;
      for (j=0; j<3; j++)
        if (Perm.class_mu_1_Proc[j]>Perm.undefined_class_mu_1_Proc)
          Perm.undefined_class_mu_1_Proc=Perm.class_mu_1_Proc[j];
    }
}
void mu_1__type_8::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };
void mu_1__type_9::Permute(PermSet& Perm, int i)
{
  static mu_1__type_9 temp("Permute_mu_1__type_9",-1);
  int j;
  for (j=0; j<3; j++)
    array[j].Permute(Perm, i);
  temp = *this;
  for (j=1; j<=3; j++)
    (*this)[j] = temp[Perm.revperm_mu_1_Proc[Perm.in_mu_1_Proc[i]][j-1]];};
void mu_1__type_9::SimpleCanonicalize(PermSet& Perm)
{ Error.Error("Internal: Simple Canonicalization of Scalarset Array\n"); };
void mu_1__type_9::Canonicalize(PermSet& Perm){};
void mu_1__type_9::SimpleLimit(PermSet& Perm){}
void mu_1__type_9::ArrayLimit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // sorting
  int count_mu_1_Proc;
  int compare;
  static mu_1_CurReq value[3];
  // limit
  bool exists;
  bool split;
  bool goodset_mu_1_Proc[3];
  bool pos_mu_1_Proc[3][3];
  // sorting mu_1_Proc
  // only if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          pos_mu_1_Proc[i][j]=FALSE;
      count_mu_1_Proc = 0;
      for (i=0; i<3; i++)
        {
          for (j=0; j<count_mu_1_Proc; j++)
            {
              compare = CompareWeight(value[j],(*this)[i+1]);
              if (compare==0)
                {
                  pos_mu_1_Proc[j][i]= TRUE;
                  break;
                }
              else if (compare>0)
                {
                  for (k=count_mu_1_Proc; k>j; k--)
                    {
                      value[k] = value[k-1];
                      for (z=0; z<3; z++)
                        pos_mu_1_Proc[k][z] = pos_mu_1_Proc[k-1][z];
                    }
                  value[j] = (*this)[i+1];
                  for (z=0; z<3; z++)
                    pos_mu_1_Proc[j][z] = FALSE;
                  pos_mu_1_Proc[j][i] = TRUE;
                  count_mu_1_Proc++;
                  break;
                }
            }
          if (j==count_mu_1_Proc)
            {
              value[j] = (*this)[i+1];
              for (z=0; z<3; z++)
                pos_mu_1_Proc[j][z] = FALSE;
              pos_mu_1_Proc[j][i] = TRUE;
              count_mu_1_Proc++;
            }
        }
    }
  // if there is more than 1 permutation in class
  if (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc>1)
    {
      // limit
      for (j=0; j<3; j++) // class priority
        {
          for (i=0; i<count_mu_1_Proc; i++) // for value priority
            {
              exists = FALSE;
              for (k=0; k<3; k++) // step through class
                goodset_mu_1_Proc[k] = FALSE;
              for (k=0; k<3; k++) // step through class
                if (pos_mu_1_Proc[i][k] && Perm.class_mu_1_Proc[k] == j)
                  {
                    exists = TRUE;
                    goodset_mu_1_Proc[k] = TRUE;
                    pos_mu_1_Proc[i][k] = FALSE;
                  }
              if (exists)
                {
                  split=FALSE;
                  for (k=0; k<3; k++)
                    if ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) 
                      split= TRUE;
                  if (split)
                    {
                      for (k=0; k<3; k++)
                        if (Perm.class_mu_1_Proc[k]>j
                            || ( Perm.class_mu_1_Proc[k] == j && !goodset_mu_1_Proc[k] ) )
                          Perm.class_mu_1_Proc[k]++;
                      Perm.undefined_class_mu_1_Proc++;
                    }
                }
            }
        }
    }
}
void mu_1__type_9::Limit(PermSet& Perm)
{
  // indexes
  int i,j,k,z;
  // while guard
  bool while_guard, while_guard_temp;
  // sorting
  static mu_1_CurReq value[3];
  // limit
  bool exists;
  bool split;
  int i0;
  int count_mu_1_Proc, oldcount_mu_1_Proc;
  bool pos_mu_1_Proc[3][3];
  bool goodset_mu_1_Proc[3];
  int count_mu_1_Value, oldcount_mu_1_Value;
  bool pos_mu_1_Value[2][2];
  bool goodset_mu_1_Value[2];
  // count_ corresponds to the number of equivalence class within the
  // scalarset value.  If count_ == size of the scalarset, then a unique
  // permutation has been found.

  // pos_ is a relation on a equivalence class number and a scalarset value.

  // initializing pos array
  for (i=0; i<3; i++)
    for (j=0; j<3; j++)
      pos_mu_1_Proc[i][j]=FALSE;
  count_mu_1_Proc = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<3; i++)
       if (Perm.class_mu_1_Proc[i] == count_mu_1_Proc)
         {
           pos_mu_1_Proc[count_mu_1_Proc][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Proc++;
      else break;
    }
  // count_ corresponds to the number of equivalence class within the
  // scalarset value.  If count_ == size of the scalarset, then a unique
  // permutation has been found.

  // pos_ is a relation on a equivalence class number and a scalarset value.

  // initializing pos array
  for (i=0; i<2; i++)
    for (j=0; j<2; j++)
      pos_mu_1_Value[i][j]=FALSE;
  count_mu_1_Value = 0;
  while (1)
    {
      exists = FALSE;
      for (i=0; i<2; i++)
       if (Perm.class_mu_1_Value[i] == count_mu_1_Value)
         {
           pos_mu_1_Value[count_mu_1_Value][i]=TRUE;
           exists = TRUE;
         }
      if (exists) count_mu_1_Value++;
      else break;
    }

  // refinement -- checking priority in general
  while_guard = FALSE;
  while_guard = while_guard || (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3);
  while_guard = while_guard || (Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2);
  while ( while_guard )
    {
      oldcount_mu_1_Proc = count_mu_1_Proc;
      oldcount_mu_1_Value = count_mu_1_Value;

      // refinement -- graph structure for two scalarsets
      //               as in array S1 of S2
      // only if there is more than 1 permutation in class
      if ( (Perm.MTO_class_mu_1_Proc() && count_mu_1_Proc<3)
           || ( Perm.MTO_class_mu_1_Value() && count_mu_1_Value<2) )
        {
          exists = FALSE;
          split = FALSE;
          for (k=0; k<3; k++) // step through class
            if ((*this)[k+1].mu_val.isundefined())
              exists = TRUE;
            else
              split = TRUE;
          if (exists && split)
            {
              for (i=0; i<count_mu_1_Proc; i++) // scan through array index priority
                for (j=0; j<count_mu_1_Value; j++) //scan through element priority
                  {
                    exists = FALSE;
                    for (k=0; k<3; k++) // initialize goodset
                      goodset_mu_1_Proc[k] = FALSE;
                    for (k=0; k<2; k++) // initialize goodset
                      goodset_mu_1_Value[k] = FALSE;
                    for (k=0; k<3; k++) // scan array index
                      // set goodsets
                      if (pos_mu_1_Proc[i][k] 
                          && !(*this)[k+1].mu_val.isundefined()
                          && pos_mu_1_Value[j][(*this)[k+1].mu_val-4])
                        {
                          exists = TRUE;
                          goodset_mu_1_Proc[k] = TRUE;
                          goodset_mu_1_Value[(*this)[k+1].mu_val-4] = TRUE;
                        }
                    if (exists)
                      {
                        // set split for the array index type
                        split=FALSE;
                        for (k=0; k<3; k++)
                          if ( pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Proc; z>i; z--)
                              for (k=0; k<3; k++)
                                pos_mu_1_Proc[z][k] = pos_mu_1_Proc[z-1][k];
                            // split pos
                            for (k=0; k<3; k++)
                              {
                                if (pos_mu_1_Proc[i][k] && !goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i][k] = FALSE;
                                if (pos_mu_1_Proc[i+1][k] && goodset_mu_1_Proc[k])
                                  pos_mu_1_Proc[i+1][k] = FALSE;
                              }
                            count_mu_1_Proc++;
                          }
                        // set split for the element type
                        split=FALSE;
                        for (k=0; k<2; k++)
                          if ( pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k] )
                            split= TRUE;
                        if (split)
                          {
                            // move following pos entries down 1 step
                            for (z=count_mu_1_Value; z>j; z--)
                              for (k=0; k<2; k++)
                                pos_mu_1_Value[z][k] = pos_mu_1_Value[z-1][k];
                            // split pos
                            for (k=0; k<2; k++)
                              {
                                if (pos_mu_1_Value[j][k] && !goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j][k] = FALSE;
                                if (pos_mu_1_Value[j+1][k] && goodset_mu_1_Value[k])
                                  pos_mu_1_Value[j+1][k] = FALSE;
                              }
                            count_mu_1_Value++;
                          }
                      }
                  }
            }
        }
      while_guard = FALSE;
      while_guard = while_guard || (oldcount_mu_1_Proc!=count_mu_1_Proc);
      while_guard = while_guard || (oldcount_mu_1_Value!=count_mu_1_Value);
      while_guard_temp = while_guard;
      while_guard = FALSE;
      while_guard = while_guard || count_mu_1_Proc<3;
      while_guard = while_guard || count_mu_1_Value<2;
      while_guard = while_guard && while_guard_temp;
    } // end while
  // enter the result into class
  if (Perm.MTO_class_mu_1_Proc())
    {
      for (i=0; i<3; i++)
        for (j=0; j<3; j++)
          if (pos_mu_1_Proc[i][j])
            Perm.class_mu_1_Proc[j] = i;
      Perm.undefined_class_mu_1_Proc=0;
      for (j=0; j<3; j++)
        if (Perm.class_mu_1_Proc[j]>Perm.undefined_class_mu_1_Proc)
          Perm.undefined_class_mu_1_Proc=Perm.class_mu_1_Proc[j];
    }
  // enter the result into class
  if (Perm.MTO_class_mu_1_Value())
    {
      for (i=0; i<2; i++)
        for (j=0; j<2; j++)
          if (pos_mu_1_Value[i][j])
            Perm.class_mu_1_Value[j] = i;
      Perm.undefined_class_mu_1_Value=0;
      for (j=0; j<2; j++)
        if (Perm.class_mu_1_Value[j]>Perm.undefined_class_mu_1_Value)
          Perm.undefined_class_mu_1_Value=Perm.class_mu_1_Value[j];
    }
}
void mu_1__type_9::MultisetLimit(PermSet& Perm)
{ Error.Error("Internal: calling MultisetLimit for scalarset array.\n"); };

/********************
 Auxiliary function for error trace printing
 ********************/
bool match(state* ns, StatePtr p)
{
  int i;
  static PermSet Perm;
  static state temp;
  StateCopy(&temp, ns);
  if (args->symmetry_reduction.value)
    {
      if (  args->sym_alg.mode == argsym_alg::Exhaustive_Fast_Canonicalize
         || args->sym_alg.mode == argsym_alg::Heuristic_Fast_Canonicalize) {
        Perm.ResetToExplicit();
        for (i=0; i<Perm.count; i++)
          if (Perm.In(i))
            {
              if (ns != workingstate)
                  StateCopy(workingstate, ns);
              
              mu_match.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_match.MultisetSort();
              mu_prevProcs.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_prevProcs.MultisetSort();
              mu_tracked.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_tracked.MultisetSort();
              mu_msg_imm_sent_set.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_msg_imm_sent_set.MultisetSort();
              mu_prevMsg.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_prevMsg.MultisetSort();
              mu_start.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_start.MultisetSort();
              mu_cur_idx.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_cur_idx.MultisetSort();
              mu_tar.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_tar.MultisetSort();
              mu_msgBufNonEmpty.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_msgBufNonEmpty.MultisetSort();
              mu_gBuf.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_gBuf.MultisetSort();
              mu_LastWrite.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_LastWrite.MultisetSort();
              mu_selc.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_selc.MultisetSort();
              mu_cur_node.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_cur_node.MultisetSort();
              mu_prevProcReq.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_prevProcReq.MultisetSort();
              mu_HomeNode.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_HomeNode.MultisetSort();
              mu_MainMemory.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_MainMemory.MultisetSort();
              mu_ackBus.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_ackBus.MultisetSort();
              mu_msgBuf.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_msgBuf.MultisetSort();
              mu_Procs.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_Procs.MultisetSort();
              mu_curRequsts.Permute(Perm,i);
              if (args->multiset_reduction.value)
                mu_curRequsts.MultisetSort();
            if (p.compare(workingstate)) {
              StateCopy(workingstate,&temp); return TRUE; }
          }
        StateCopy(workingstate,&temp);
        return FALSE;
      }
      else {
        Perm.ResetToSimple();
        Perm.SimpleToOne();
        if (ns != workingstate)
          StateCopy(workingstate, ns);

          mu_match.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_match.MultisetSort();
          mu_prevProcs.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_prevProcs.MultisetSort();
          mu_tracked.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_tracked.MultisetSort();
          mu_msg_imm_sent_set.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_msg_imm_sent_set.MultisetSort();
          mu_prevMsg.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_prevMsg.MultisetSort();
          mu_start.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_start.MultisetSort();
          mu_cur_idx.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_cur_idx.MultisetSort();
          mu_tar.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_tar.MultisetSort();
          mu_msgBufNonEmpty.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_msgBufNonEmpty.MultisetSort();
          mu_gBuf.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_gBuf.MultisetSort();
          mu_LastWrite.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_LastWrite.MultisetSort();
          mu_selc.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_selc.MultisetSort();
          mu_cur_node.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_cur_node.MultisetSort();
          mu_prevProcReq.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_prevProcReq.MultisetSort();
          mu_HomeNode.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_HomeNode.MultisetSort();
          mu_MainMemory.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_MainMemory.MultisetSort();
          mu_ackBus.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_ackBus.MultisetSort();
          mu_msgBuf.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_msgBuf.MultisetSort();
          mu_Procs.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_Procs.MultisetSort();
          mu_curRequsts.Permute(Perm,0);
          if (args->multiset_reduction.value)
            mu_curRequsts.MultisetSort();
        if (p.compare(workingstate)) {
          StateCopy(workingstate,&temp); return TRUE; }

        while (Perm.NextPermutation())
          {
            if (ns != workingstate)
              StateCopy(workingstate, ns);
              
              mu_match.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_match.MultisetSort();
              mu_prevProcs.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_prevProcs.MultisetSort();
              mu_tracked.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_tracked.MultisetSort();
              mu_msg_imm_sent_set.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_msg_imm_sent_set.MultisetSort();
              mu_prevMsg.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_prevMsg.MultisetSort();
              mu_start.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_start.MultisetSort();
              mu_cur_idx.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_cur_idx.MultisetSort();
              mu_tar.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_tar.MultisetSort();
              mu_msgBufNonEmpty.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_msgBufNonEmpty.MultisetSort();
              mu_gBuf.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_gBuf.MultisetSort();
              mu_LastWrite.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_LastWrite.MultisetSort();
              mu_selc.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_selc.MultisetSort();
              mu_cur_node.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_cur_node.MultisetSort();
              mu_prevProcReq.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_prevProcReq.MultisetSort();
              mu_HomeNode.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_HomeNode.MultisetSort();
              mu_MainMemory.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_MainMemory.MultisetSort();
              mu_ackBus.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_ackBus.MultisetSort();
              mu_msgBuf.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_msgBuf.MultisetSort();
              mu_Procs.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_Procs.MultisetSort();
              mu_curRequsts.Permute(Perm,0);
              if (args->multiset_reduction.value)
                mu_curRequsts.MultisetSort();
            if (p.compare(workingstate)) {
              StateCopy(workingstate,&temp); return TRUE; }
          }
        StateCopy(workingstate,&temp);
        return FALSE;
      }
    }
  if (!args->symmetry_reduction.value
      && args->multiset_reduction.value)
    {
      if (ns != workingstate)
          StateCopy(workingstate, ns);
      mu_match.MultisetSort();
      mu_prevProcs.MultisetSort();
      mu_tracked.MultisetSort();
      mu_msg_imm_sent_set.MultisetSort();
      mu_prevMsg.MultisetSort();
      mu_start.MultisetSort();
      mu_cur_idx.MultisetSort();
      mu_tar.MultisetSort();
      mu_msgBufNonEmpty.MultisetSort();
      mu_gBuf.MultisetSort();
      mu_LastWrite.MultisetSort();
      mu_selc.MultisetSort();
      mu_cur_node.MultisetSort();
      mu_prevProcReq.MultisetSort();
      mu_HomeNode.MultisetSort();
      mu_MainMemory.MultisetSort();
      mu_ackBus.MultisetSort();
      mu_msgBuf.MultisetSort();
      mu_Procs.MultisetSort();
      mu_curRequsts.MultisetSort();
      if (p.compare(workingstate)) {
        StateCopy(workingstate,&temp); return TRUE; }
      StateCopy(workingstate,&temp);
      return FALSE;
    }
  return (p.compare(ns));
}

/********************
 Canonicalization by fast exhaustive generation of
 all permutations
 ********************/
void SymmetryClass::Exhaustive_Fast_Canonicalize(state* s)
{
  int i;
  static state temp;
  Perm.ResetToExplicit();

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_match.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_match.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_prevProcs.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_prevProcs.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_tracked.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_tracked.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_msg_imm_sent_set.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_msg_imm_sent_set.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_prevMsg.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_prevMsg.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_start.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_start.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_cur_idx.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_cur_idx.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_tar.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_tar.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_msgBufNonEmpty.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_msgBufNonEmpty.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_gBuf.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_gBuf.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_LastWrite.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_LastWrite.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_selc.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_selc.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_cur_node.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_cur_node.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_prevProcReq.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_prevProcReq.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_HomeNode.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_HomeNode.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_MainMemory.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_MainMemory.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_ackBus.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_ackBus.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_msgBuf.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_msgBuf.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_Procs.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_Procs.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_curRequsts.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_curRequsts.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

};

/********************
 Canonicalization by fast simple variable canonicalization,
 fast simple scalarset array canonicalization,
 fast restriction on permutation set with simple scalarset array of scalarset,
 and fast exhaustive generation of
 all permutations for other variables
 ********************/
void SymmetryClass::Heuristic_Fast_Canonicalize(state* s)
{
  int i;
  static state temp;

  Perm.ResetToSimple();

  mu_gBuf.SimpleCanonicalize(Perm);

  mu_LastWrite.SimpleCanonicalize(Perm);

  mu_selc.SimpleCanonicalize(Perm);

  mu_cur_node.SimpleCanonicalize(Perm);

  mu_prevProcReq.SimpleCanonicalize(Perm);

  mu_HomeNode.SimpleCanonicalize(Perm);

  mu_MainMemory.SimpleCanonicalize(Perm);

  mu_ackBus.Canonicalize(Perm);

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.Limit(Perm);
  }

  Perm.SimpleToExplicit();

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_msgBuf.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_msgBuf.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_Procs.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_Procs.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

  StateCopy(&temp, workingstate);
  ResetBestResult();
  for (i=0; i<Perm.count; i++)
    if (Perm.In(i))
      {
        StateCopy(workingstate, &temp);
        mu_curRequsts.Permute(Perm,i);
        if (args->multiset_reduction.value)
          mu_curRequsts.MultisetSort();
        SetBestResult(i, workingstate);
      }
  StateCopy(workingstate, &BestPermutedState);

};

/********************
 Canonicalization by fast simple variable canonicalization,
 fast simple scalarset array canonicalization,
 fast restriction on permutation set with simple scalarset array of scalarset,
 and fast exhaustive generation of
 all permutations for other variables
 and use less local memory
 ********************/
void SymmetryClass::Heuristic_Small_Mem_Canonicalize(state* s)
{
  unsigned long cycle;
  static state temp;

  Perm.ResetToSimple();

  mu_gBuf.SimpleCanonicalize(Perm);

  mu_LastWrite.SimpleCanonicalize(Perm);

  mu_selc.SimpleCanonicalize(Perm);

  mu_cur_node.SimpleCanonicalize(Perm);

  mu_prevProcReq.SimpleCanonicalize(Perm);

  mu_HomeNode.SimpleCanonicalize(Perm);

  mu_MainMemory.SimpleCanonicalize(Perm);

  mu_ackBus.Canonicalize(Perm);

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.Limit(Perm);
  }

  Perm.SimpleToOne();

  StateCopy(&temp, workingstate);
  ResetBestResult();
  mu_msgBuf.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_msgBuf.MultisetSort();
  mu_Procs.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_Procs.MultisetSort();
  mu_curRequsts.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_curRequsts.MultisetSort();
  BestPermutedState = *workingstate;
  BestInitialized = TRUE;

  cycle=1;
  while (Perm.NextPermutation())
    {
      if (args->perm_limit.value != 0
          && cycle++ >= args->perm_limit.value) break;
      StateCopy(workingstate, &temp);
      mu_msgBuf.Permute(Perm,0);
      if (args->multiset_reduction.value)
        mu_msgBuf.MultisetSort();
      mu_Procs.Permute(Perm,0);
      if (args->multiset_reduction.value)
        mu_Procs.MultisetSort();
      mu_curRequsts.Permute(Perm,0);
      if (args->multiset_reduction.value)
        mu_curRequsts.MultisetSort();
      switch (StateCmp(workingstate, &BestPermutedState)) {
      case -1:
        BestPermutedState = *workingstate;
        break;
      case 1:
        break;
      case 0:
        break;
      default:
        Error.Error("funny return value from StateCmp");
      }
    }
  StateCopy(workingstate, &BestPermutedState);

};

/********************
 Normalization by fast simple variable canonicalization,
 fast simple scalarset array canonicalization,
 fast restriction on permutation set with simple scalarset array of scalarset,
 and for all other variables, pick any remaining permutation
 ********************/
void SymmetryClass::Heuristic_Fast_Normalize(state* s)
{
  int i;
  static state temp;

  Perm.ResetToSimple();

  mu_gBuf.SimpleCanonicalize(Perm);

  mu_LastWrite.SimpleCanonicalize(Perm);

  mu_selc.SimpleCanonicalize(Perm);

  mu_cur_node.SimpleCanonicalize(Perm);

  mu_prevProcReq.SimpleCanonicalize(Perm);

  mu_HomeNode.SimpleCanonicalize(Perm);

  mu_MainMemory.SimpleCanonicalize(Perm);

  mu_ackBus.Canonicalize(Perm);

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.ArrayLimit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_msgBuf.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_Procs.Limit(Perm);
  }

  if (Perm.MoreThanOneRemain()) {
    mu_curRequsts.Limit(Perm);
  }

  Perm.SimpleToOne();

  mu_msgBuf.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_msgBuf.MultisetSort();

  mu_Procs.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_Procs.MultisetSort();

  mu_curRequsts.Permute(Perm,0);
  if (args->multiset_reduction.value)
    mu_curRequsts.MultisetSort();

};

/********************
  Include
 ********************/
#include "mu_epilog.hpp"
