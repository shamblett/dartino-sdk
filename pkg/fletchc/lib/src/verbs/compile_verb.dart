// Copyright (c) 2015, the Fletch project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE.md file.

library fletchc.verbs.compile_verb;

import 'infrastructure.dart';

import '../driver/developer.dart' as developer;

import 'documentation.dart' show
    compileDocumentation;

const Action compileAction = const Action(
    compile, compileDocumentation, requiresSession: true,
    requiredTarget: TargetKind.FILE);

Future<int> compile(AnalyzedSentence sentence, VerbContext context) {
  bool analyzeOnly = sentence.options.analyzeOnly;
  bool fatalIncrementalFailures = sentence.options.fatalIncrementalFailures;
  return context.performTaskInWorker(
      new CompileTask(
          sentence.targetUri, analyzeOnly, fatalIncrementalFailures));
}

class CompileTask extends SharedTask {
  // Keep this class simple, see note in superclass.

  final Uri script;

  final bool analyzeOnly;

  final bool fatalIncrementalFailures;

  const CompileTask(
      this.script, this.analyzeOnly, this.fatalIncrementalFailures);

  Future<int> call(
      CommandSender commandSender,
      StreamIterator<Command> commandIterator) {
    return compileTask(script, analyzeOnly, fatalIncrementalFailures);
  }
}

Future<int> compileTask(
    Uri script, bool analyzeOnly, bool fatalIncrementalFailures) {
  return developer.compile(
      script, SessionState.current, analyzeOnly: analyzeOnly,
      fatalIncrementalFailures: fatalIncrementalFailures);
}
