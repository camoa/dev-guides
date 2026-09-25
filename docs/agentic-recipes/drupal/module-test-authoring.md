---
# Routing block — an orchestrator reads to here and decides.
name: drupal_module_test_authoring
capability: drupal-module-test-authoring
description: Use when a Drupal module needs tests written or extended — deciding which kind of test each behaviour gets, writing it to the conventions current core and PHPUnit enforce, and proving the run actually collected it.
# Metadata — read only after a match.
label: Drupal module test authoring
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/testing/framework-selection-decision-matrix
  - drupal/testing/phpunit-unit-tests
  - drupal/testing/phpunit-kernel-tests
  - drupal/testing/phpunit-functional-tests
  - drupal/testing/phpunit-functionaljavascript-tests
  - drupal/testing/testing-infrastructure-setup
  - drupal/testing/running-debugging-tests
  - drupal/tdd/test-type-decision-matrix
  - drupal/tdd/nightwatch-testing
drupal_compatibility: "^10.3 || ^11"
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Give a module the tests its behaviours deserve: one kind chosen per behaviour rather than one kind for the module, written so the runner collects them, and proved by a run whose output the author read. The recipe owns the choice and the proof. The mechanics of each kind — base class, directory, namespace, setup calls — belong to the guides it cites and are not restated here.

## Opinion

**Start at Kernel and move only for a reason.** A Kernel test boots the container, installs the modules it names, and reaches the database, which covers most of what a Drupal module is: services, entities, plugins, hooks, configuration. Move down to Unit only when the code under test touches no container at all. Move up to Functional only for a reason this recipe names. The two mature contrib modules surveyed for this recipe write Kernel over Functional by 141 to 2 and 194 to 65, and core is converting Functional tests to Kernel where coverage allows because the conversion cuts about three quarters of the runtime.

**From Drupal 11.4, needing to read a page is no longer a reason to go Functional.** `KernelTestBase` uses `Drupal\Tests\HttpKernelUiHelperTrait`, so every Kernel test has `drupalGet()`, `clickLink()` and `assertSession()` without opting in, and sends its request through the HTTP kernel. What a Kernel test still cannot do: submit a form, log in, run JavaScript, or answer anything that needs a real web server — `submitForm()` and `drupalLogin()` exist on `BrowserTestBase` only. Those four are the reasons to go Functional, and the only ones. On Drupal 10 the older rule holds: no `drupalGet()` at all, so reading a page is Functional's job there.

**A kind of test the project's pipeline does not run is worse than no test.** It is written, it is reviewed, it reports nothing, and it looks like coverage. One of the surveyed modules refuses Build, FunctionalJavascript and Component tests through its own coding-standards rule for exactly this reason, saying so in the rule: without the guard "tests of these types would silently never execute, appearing to pass in CI when they have not run at all." Before choosing a kind, establish that the pipeline runs it. If it does not, either add pipeline support first or choose a kind that runs.

**Read the status line, never the exit code alone.** A run that selected nothing prints `No tests executed!` and exits 0 — it did not pass, it did not run, and the exit code says nothing about it. `FAILURES!` means a test ran and an assertion did not hold. `ERRORS!` means something broke before the assertion, whatever the assertion count. An author who reports "tests pass" without quoting the status line has not checked.

**Cite the skill for the traps it already carries.** The `drupal-automated-testing` skill in `ai_best_practices` is the current source on the unasserted `waitForElement`, the dual-container trap in Functional tests, and the per-kind namespaces including the `FunctionalJavascript` capitalisation. This recipe does not restate them. It parts company with that skill in two places. The skill makes Functional the default and this recipe starts at Kernel, for the reasons above. And from Drupal 11.4 reading a page stopped being a reason to reach for Functional, which the skill predates.

## Preconditions

- Drupal 10.3+ or 11.x, Composer-managed, with core's development dependencies installed so PHPUnit resolves.
- A `phpunit.xml` the project owns, at the project root beside `composer.json`, with its `bootstrap=`, its testsuite directories and its browser-output directory written for that location, and `SIMPLETEST_DB` filled in. `drupal/testing/testing-infrastructure-setup` is the reference; a run against core's own configuration is not this recipe's form.
- The module exists and its `.info.yml` is in place. Nothing here scaffolds a module, and a test cannot be watched to fail against a module the extension scan cannot find.
- For Kernel and above, a database the runner can reach. For Functional, a served site. For FunctionalJavascript, a WebDriver endpoint.
- Knowledge of which kinds the project's pipeline actually runs. If that cannot be established, this recipe's first sequence step surfaces it as a finding rather than guessing.
- DDEV runs the project; the verifier runs PHPUnit through `ddev exec`.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
core_version: string           # the project's Drupal version, e.g. 11.4.5; the choice in
                               # sequence step 2 branches on 11.4

module:
  name: string                 # machine name
  path: string                 # path to the module, relative to the docroot

behaviours:                    # one entry per thing to be proved
  - id: string                 # caller's identifier, echoed in the report
    statement: string          # what must be true, in one sentence
    touches:                   # what the behaviour reaches, used to choose the kind
      container: boolean       # needs services, entities, config or the database
      page: boolean            # a response must be read
      form_submission: boolean # a form must be submitted, or a user logged in
      served_site: boolean     # needs a real web server: a redirect, a real session,
                               # a header only the server sets
      javascript: boolean      # behaviour only exists with JS or Ajax running

pipeline_runs:                 # the kinds the project's pipeline executes
  - string                     # unit | kernel | functional | functional-javascript

existing_tests: boolean        # whether the module already has a test suite to extend
```

## Sequence

1. **Establish what the pipeline runs.** Read the project's pipeline configuration and record which kinds it executes. A kind absent from it is unavailable to this recipe; report that as a finding before any test is written, because a test of that kind would never run.

2. **Choose the kind per behaviour, not per module.** Ask these in order and stop at the first yes. The order is the rule: a behaviour that is both an Ajax interaction and a form submission is FunctionalJavascript, because the first question catches it.

   1. Does the behaviour need JavaScript or Ajax running? → FunctionalJavascript.
   2. Does it submit a form, need a logged-in session, or need a real web server? → Functional.
   3. Does it read a page, on a project whose `core_version` is below 11.4? → Functional, because a Kernel test has no `drupalGet()` there.
   4. Does it reach the container — a service, an entity, configuration or the database — or does it read a page on 11.4 or later? → Kernel.
   5. Otherwise → Unit.

   Record the reason beside the choice; a choice with no reason is a default in disguise. `drupal/testing/framework-selection-decision-matrix` and `drupal/tdd/test-type-decision-matrix` carry the long form.

3. **Write the test to the kind's guide.** `drupal/testing/phpunit-unit-tests`, `drupal/testing/phpunit-kernel-tests`, `drupal/testing/phpunit-functional-tests` and `drupal/testing/phpunit-functionaljavascript-tests` each carry the base class, directory, namespace and setup calls. Four things this recipe requires on top, because the runner or core enforces them and a guide example is easy to copy past: every Kernel, Functional and FunctionalJavascript class declares `#[RunTestsInSeparateProcesses]` and no Unit class does; the attribute is not inherited, so a project's own test base class cannot carry it for its subclasses; every data provider is `static` and named by `#[DataProvider]`; and metadata goes in attributes, not doc-comments.

4. **Watch each new test fail before the code exists, and read why it failed.** A test that has never been seen red proves nothing about the behaviour. The failure must be an assertion that ran and did not hold, not a harness error and not a run that selected nothing. For a class that does not exist yet, open the test with one assertion that names it so the first run fails an assertion instead of erroring in autoload.

5. **Run, and read the status line.** Run the narrowest scope that covers the new tests, with the project's own configuration named. Quote the status line and the counts in the report. `No tests executed!` is not a pass. A path argument and `--testsuite` do not combine — the path wins and the flag is ignored — so pass one or the other, never both.

6. **Report per behaviour.** Each behaviour in the input gets its chosen kind, the reason, the test's file and method, the status line of the run that proved it, and for a behaviour no test covers, why not. A behaviour whose kind the pipeline does not run is reported as uncovered, whatever was written for it.

## Data flow

```
input:  core_version, module, behaviours[], pipeline_runs[],     supplied by the caller
        existing_tests

step 1: the project's pipeline configuration    → kinds available; kinds refused, as findings
step 2: behaviours[].touches + core_version     → kind per behaviour + recorded reason
step 3: the kind's guide + this recipe's four   → test files under <module>/tests/src/<Kind>/
        requirements
step 4: the runner, narrowest scope             → a red per new test, with its status line
step 5: the runner, narrowest scope             → the status line and counts per run
step 6: everything above                        → report, one row per input behaviour
```

## State-awareness contract

Re-running this recipe over a module that already has tests extends rather than replaces. A behaviour whose test already exists and already passes is left alone and reported as covered; its file is not rewritten to this recipe's shape unless it is the behaviour being changed. Test files this recipe writes are the only files it writes: it never edits production code to make a test pass, and it never scaffolds a module. Step 4 leaves the module red by design, and the red is the recipe's output, not a failure of it. Nothing here writes to the project's `phpunit.xml`; a configuration that cannot run the chosen kind is a precondition failure, reported, not repaired.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only. Every entry calls `.aida/module-test-authoring/verify.sh`, the script in `## Files`, with the files the order owns. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: separate-process-attribute
    kind: config-assert
    run: bash .aida/module-test-authoring/verify.sh attributes {paths}
    pass: stdout empty
  - id: static-data-providers
    kind: config-assert
    run: bash .aida/module-test-authoring/verify.sh providers {paths}
    pass: stdout empty
  - id: no-doc-comment-metadata
    kind: config-assert
    run: bash .aida/module-test-authoring/verify.sh metadata {paths}
    pass: stdout empty
  - id: tests-run
    kind: live-site
    run: bash .aida/module-test-authoring/verify.sh run {paths}
    pass: stdout empty
  - id: assertion-can-fail
    kind: self-fixture
    run: bash .aida/module-test-authoring/verify.sh mutant {paths}
    pass: stdout empty

What the entries do not prove, and where the proof is:

- Every entry reads only the `*Test.php` files under `tests/src/` among the order's files. With none, it prints a violation, so an order that owns no test file fails rather than passing on an empty list.
- The test kind comes from the directory after `tests/src/`, not from the base class, because a project's own base class hides core's. `separate-process-attribute` skips abstract classes and every directory other than `Unit`, `Kernel`, `Functional` and `FunctionalJavascript`. It accepts the attribute with its `use` statement, a grouped `use`, or a fully qualified name. A commented-out attribute or `use` does not count.
- `static-data-providers` reads `#[DataProvider('name')]` and `#[DataProvider(methodName: 'name')]`. It fails a provider that is not static or not public. It also fails one that is not declared in the same file, including one inherited from a base class. PHPUnit accepts an inherited provider, so this entry is stricter than the runner. `#[DataProviderExternal]` is not checked.
- `no-doc-comment-metadata` fails every tag PHPUnit 11.5's annotation parser reads, not only `@group`, `@covers`, `@coversDefaultClass` and `@dataProvider`. It also fails such a tag on a `*` line of a plain `/* */` comment.
- `tests-run` runs `ddev exec vendor/bin/phpunit -c phpunit.xml` over the test files. It passes on a status line of `FAILURES!` or one starting `OK (`. `ERRORS!`, `No tests executed!`, `OK, but there were issues!`, `OK, but some tests were skipped!`, a PHP fatal error, a missing status line, and an `OK (` whose exit code is not 0 all fail it. Kernel and above need a database, Functional a served site, and FunctionalJavascript a WebDriver endpoint. Where one is missing the entry fails, and that is a correct fail-close.
- `tests-run` accepts `FAILURES!` because Sequence step 4 leaves each new test red on purpose, failing an assertion before its code exists. It proves the tests were collected and their assertions ran, not that the behaviour holds. A test that errors instead of failing is still refused, as step 4 requires.
- `assertion-can-fail` picks the first Unit or Kernel test file, or the first test file when the order owns neither kind. No input names "one behaviour of the caller's choosing", so the script chooses. It first runs that file unmutated. `FAILURES!` passes the entry at once, because an assertion is already shown to fail, as step 4 leaves it. Any status other than `FAILURES!` or one starting `OK (` fails the entry, and so does an `OK (` whose exit code is not 0. On `OK (`, it inverts the first `assertTrue`, `assertFalse`, `assertSame`, `assertEquals` or `assertNull` call, or its `Not` form, in a copy under `.aida/module-test-authoring/mutant/`. It runs the copy, passes only on `FAILURES!`, and removes the copy. An assertion in a helper that no test calls leaves the copy green, and the entry fails. A red file proves that one assertion fails, not which one.
- No entry checks that the report accounts for every behaviour, because the report has no defined file. Sequence step 6 carries that contract.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. `bash` runs it from the project root, with the order's files as its arguments.

```sh .aida/module-test-authoring/verify.sh
# Verifier checks for module-test-authoring.
# bash verify.sh attributes|providers|metadata|run|mutant <file>...
# Reads only the *Test.php files under tests/src/ among its arguments. The test
# kind is the directory after tests/src/, because a project's own base class
# hides the core one. Prints one line per violation and exits 1 when it printed
# any; exits 2 on a usage error. Uses the grep on PATH with POSIX ERE only.
check=${1:-}
[ $# -gt 0 ] && shift
case $check in
  attributes|providers|metadata|run|mutant) ;;
  *) echo "usage: verify.sh attributes|providers|metadata|run|mutant <file>..." >&2; exit 2 ;;
esac

v=0
say() { printf '%s\n' "$*"; v=1; }
kind_of() { rest=${1#*tests/src/}; printf '%s' "${rest%%/*}"; }
# The lines of $1 outside a comment. A line opening with //, with # but not #[,
# or with /*, and every line up to the closing */, is dropped whole.
code_of() {
  awk '
    inc { if ($0 ~ /\*\//) inc = 0; next }
    /^[[:space:]]*\/\*/ { if ($0 !~ /\*\//) inc = 1; next }
    /^[[:space:]]*(\/\/|#($|[^[]))/ { next }
    { print }
  ' "$1"
}

tests=()
for f in "$@"; do
  case $f in
    tests/src/*Test.php|*/tests/src/*Test.php)
      if [ -f "$f" ]; then tests+=("$f"); else say "$f: not found"; fi ;;
  esac
done
if [ ${#tests[@]} -eq 0 ]; then
  say "$check: the order owns no *Test.php file under tests/src/, so there is nothing to check"
  exit 1
fi

phpunit() { ddev exec vendor/bin/phpunit -c phpunit.xml --colors=never "$@" 2>&1; }
status_line() { printf '%s\n' "$1" | grep -E '^(OK|OK, but|FAILURES!|ERRORS!|No tests executed!)' | tail -n 1; }

case $check in
attributes)
  attr='#\[([^]]*[[:space:],])?\\?(PHPUnit\\Framework\\Attributes\\)?RunTestsInSeparateProcesses([],([:space:]]|$)'
  for f in "${tests[@]}"; do
    kind=$(kind_of "$f")
    code=$(code_of "$f")
    has=no
    printf '%s\n' "$code" | grep -Eq "$attr" && has=yes
    case $kind in
      Kernel|Functional|FunctionalJavascript)
        printf '%s\n' "$code" | grep -Eq '^[[:space:]]*([a-z]+[[:space:]]+)*abstract[[:space:]]+([a-z]+[[:space:]]+)*class[[:space:]]' && continue
        imported=no
        printf '%s\n' "$code" | grep -Eq '#\[([^]]*[[:space:],])?\\PHPUnit\\Framework\\Attributes\\RunTestsInSeparateProcesses' && imported=yes
        printf '%s\n' "$code" | grep -Eq '^use[[:space:]]+PHPUnit\\Framework\\Attributes\\(RunTestsInSeparateProcesses[[:space:]]*;|\{[^}]*RunTestsInSeparateProcesses)' && imported=yes
        if [ $has = no ]; then
          say "$f: a $kind class without #[RunTestsInSeparateProcesses]; the attribute is not inherited"
        elif [ $imported = no ]; then
          say "$f: #[RunTestsInSeparateProcesses] without its use statement or a fully qualified name"
        fi ;;
      Unit)
        [ $has = yes ] && say "$f: a Unit class declares #[RunTestsInSeparateProcesses]; Unit tests take none" ;;
    esac
  done ;;

providers)
  for f in "${tests[@]}"; do
    code=$(code_of "$f")
    for name in $(printf '%s\n' "$code" | sed -n "s/.*DataProvider([[:space:]]*\(methodName:[[:space:]]*\)\{0,1\}[\"']\([A-Za-z0-9_]*\)[\"'][[:space:]]*).*/\2/p" | sort -u); do
      decl=$(printf '%s\n' "$code" | grep -E "function[[:space:]]+$name[[:space:]]*\(" | head -n 1)
      mods=${decl%%function*}
      if [ -z "$decl" ]; then
        say "$f: data provider $name() is not declared in this file"
      else
        case " $mods " in *[[:space:]]static[[:space:]]*) ;; *) say "$f: data provider $name() is not static" ;; esac
        case " $mods " in *[[:space:]]public[[:space:]]*) ;; *) say "$f: data provider $name() is not public" ;; esac
      fi
    done
  done ;;

metadata)
  tags='after|afterClass|backupGlobals|backupStaticAttributes|backupStaticProperties|before|beforeClass|covers|coversDefaultClass|coversNothing|dataProvider|depends|doesNotPerformAssertions|excludeGlobalVariableFromBackup|excludeStaticPropertyFromBackup|group|large|medium|postCondition|preCondition|preserveGlobalState|requires|runClassInSeparateProcess|runInSeparateProcess|runTestsInSeparateProcesses|small|test|testdox|testWith|ticket|uses|usesDefaultClass'
  for f in "${tests[@]}"; do
    hits=$(grep -nE "^[[:space:]]*(/\*\*|\*)[[:space:]]*@($tags)([[:space:]]|\*|$)" "$f")
    [ -z "$hits" ] && continue
    while IFS= read -r line; do
      say "$f:${line%%:*}: doc-comment metadata; write it as an attribute:${line#*:}"
    done <<EOF
$hits
EOF
  done ;;

run)
  out=$(phpunit "${tests[@]}"); rc=$?
  line=$(status_line "$out")
  if printf '%s\n' "$out" | grep -Eq 'Fatal error'; then
    say "run: phpunit hit a PHP fatal error"
  fi
  case $line in
    OK\ \(*) [ "$rc" -eq 0 ] || say "run: phpunit printed '$line' but exited $rc" ;;
    FAILURES!) ;;
    *) say "run: phpunit printed '${line:-no status line}', not OK or FAILURES!" ;;
  esac ;;

mutant)
  target=
  for f in "${tests[@]}"; do
    case $(kind_of "$f") in Unit|Kernel) target=$f; break ;; esac
  done
  [ -n "$target" ] || target=${tests[0]}
  # A red target already shows an assertion failing; only a green one is mutated.
  out=$(phpunit "$target"); rc=$?
  base=$(status_line "$out")
  case $base in
    FAILURES!) ;;
    OK\ \(*)
      if [ "$rc" -ne 0 ]; then
        say "mutant: $target unmutated printed '$base' but exited $rc"
      else
        dir=.aida/module-test-authoring/mutant
        copy=$dir/$(basename "$target")
        mkdir -p "$dir" || exit 2
        trap 'rm -f "$copy"; rmdir "$dir" 2>/dev/null' EXIT
        awk '
          !done && match($0, /assert(Not)?(True|False|Same|Equals|Null)\(/) {
            a = substr($0, RSTART, RLENGTH)
            if (a == "assertTrue(") b = "assertFalse("
            else if (a == "assertFalse(") b = "assertTrue("
            else if (a ~ /^assertNot/) b = "assert" substr(a, 10)
            else b = "assertNot" substr(a, 7)
            $0 = substr($0, 1, RSTART - 1) b substr($0, RSTART + RLENGTH)
            done = 1
          }
          { print }
          END { if (!done) exit 3 }
        ' "$target" > "$copy"
        if [ $? -ne 0 ]; then
          say "mutant: $target has no assertTrue, assertFalse, assertSame, assertEquals or assertNull call to invert"
        else
          out=$(phpunit "$copy")
          line=$(status_line "$out")
          case $line in
            FAILURES!) ;;
            *) say "mutant: $target with its first assertion inverted printed '${line:-no status line}', not FAILURES!" ;;
          esac
        fi
      fi ;;
    *) say "mutant: $target unmutated printed '${base:-no status line}', not OK or FAILURES!" ;;
  esac ;;
esac

[ $v -eq 0 ] || exit 1
```

## References

| Source | What it settles |
|---|---|
| [Framework selection decision matrix](../../drupal/testing/framework-selection-decision-matrix.md), [Test type decision matrix](../../drupal/tdd/test-type-decision-matrix.md) | The long form of the choice this recipe sequences |
| [Unit](../../drupal/testing/phpunit-unit-tests.md), [Kernel](../../drupal/testing/phpunit-kernel-tests.md), [Functional](../../drupal/testing/phpunit-functional-tests.md), [FunctionalJavascript](../../drupal/testing/phpunit-functionaljavascript-tests.md) | Base class, directory, namespace, setup calls and the traps of each kind |
| [Testing infrastructure setup](../../drupal/testing/testing-infrastructure-setup.md), [Running and debugging tests](../../drupal/testing/running-debugging-tests.md) | Where `phpunit.xml` lives, what must be rewritten in it, and how a run is scoped |
| [Nightwatch testing](../../drupal/tdd/nightwatch-testing.md) | Why JavaScript coverage is a FunctionalJavascript test rather than a Nightwatch one, and what core's replacement policy has and has not landed |
| `ai_best_practices`, skill `drupal-automated-testing` | The unasserted `waitForElement`, the dual-container trap, the per-kind namespaces. Cited, not restated; this recipe differs from it only on reading a page from a Kernel test, and only from Drupal 11.4 |
| Drupal core 11.4.5 — `KernelTestBase`, `HttpKernelUiHelperTrait`, `BrowserTestBase` | That a Kernel test can read a page but cannot submit a form or log in; that omitting the separate-processes attribute is deprecated as of 11.3 and throws in 12 |
| PHPUnit 11.5.56 | That a non-static data provider asserts nothing; that a run selecting nothing prints `No tests executed!` and still exits 0; that doc-comment metadata is deprecated; that a path argument overrides `--testsuite` |
