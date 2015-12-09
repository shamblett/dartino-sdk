// Copyright (c) 2015, the Fletch project authors. Please see the AUTHORS file
// for details. All rights reserved. Use of this source code is governed by a
// BSD-style license that can be found in the LICENSE.md file.

// Looking up a library should not make the symbols reachable from main lookup
// unless we explicitly pass the global flag.

import 'dart:fletch.ffi';
import "package:expect/expect.dart";

bool isArgumentError(e) => e is ArgumentError;

void main() {
  var libPath = ForeignLibrary.bundleLibraryName('ffi_test_library');
  ForeignLibrary fl = new ForeignLibrary.fromName(libPath);
  Expect.throws(
      () => ForeignLibrary.main.lookup('memuint32'),
      isArgumentError);
  fl.close();

  ForeignLibrary flGlobal = new ForeignLibrary.fromName(libPath, global: true);
  Expect.isTrue(ForeignLibrary.main.lookup('memuint32').address > 0);
}
