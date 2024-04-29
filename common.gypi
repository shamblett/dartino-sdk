# Copyright (c) 2015, the Dartino project authors. Please see the AUTHORS file
# for details. All rights reserved. Use of this source code is governed by a
# BSD-style license that can be found in the LICENSE.md file.

# TODO(ahe): Move this file elsewhere?

{
  'variables': {
    'clang%': '0',

    'common_gcc_warning_flags': [
      '-Wall',
      '-Wextra', # Also known as -W.
      '-Wno-unused-parameter',
      '-Wno-format',
      '-Wno-comment',
    ],

    'common_gcc_cflags_c': [
      '-fdata-sections',
      '-ffunction-sections',
      '-fvisibility=hidden',
    ],

    'common_gcc_cflags_cc': [
      '-std=c++11',
      '<@(common_gcc_cflags_c)',
      '-Wno-invalid-offsetof',
    ],

    'LK_PATH%': 'third_party/lk/lk-upstream',

    'LK_USE_DEPS_ARM_GCC%': '1',

    'mbed_path': '<(DEPTH)/third_party/mbed/build/',

    'posix%': 1,

    'conditions': [
      [ 'OS=="mac"', {
        # TODO(zerny): Redirect stderr to work around gyp regarding a non-empty
        # stderr as a failed command. This should be replaced by a custom script
        # that retains stderr in case the command actually fails.
        'ios_sdk_path%': '<!(xcrun --sdk iphoneos --show-sdk-path 2>/dev/null)',
        'ios_sim_sdk_path%':
            '<!(xcrun --sdk iphonesimulator --show-sdk-path 2>/dev/null)',
      }],
    ],
  },

  'conditions': [
    [ 'OS!="win"', {
      'make_global_settings': [
        [ 'CC', 'tools/cc_wrapper.py' ],
        [ 'CXX', 'tools/cxx_wrapper.py' ],
        [ 'LINK', 'tools/cc_wrapper.py' ],
      ],
    }],
  ],

  'target_defaults': {
    'msvs_cygwin_dirs': ['<(DEPTH)/third_party/cygwin'],
    'msvs_cygwin_shell': 0,

    'configurations': {

      'dartino_base': {
        'abstract': 1,

        'defines': [
          'DARTINO_ENABLE_LIVE_CODING',
          'DARTINO_ENABLE_DEBUGGING',
          'DARTINO_ENABLE_FFI',
          'DARTINO_ENABLE_NATIVE_PROCESSES',
          'DARTINO_ENABLE_PRINT_INTERCEPTORS',
        ],

        'xcode_settings': {
          # Settings for Xcode and ninja. Huh? Yeah, GYP is awesome!

          'GCC_C_LANGUAGE_STANDARD': 'ansi',
          'GCC_TREAT_WARNINGS_AS_ERRORS': 'NO', # -Werror
          'GCC_WARN_NON_VIRTUAL_DESTRUCTOR': 'NO', # -Wno-non-virtual-dtor
          'GCC_ENABLE_CPP_RTTI': 'NO', # -fno-rtti
          'GCC_ENABLE_CPP_EXCEPTIONS': 'NO', # -fno-exceptions
          'DEAD_CODE_STRIPPING': 'YES', # -Wl,-dead_strip (mac --gc-sections)

          'OTHER_CPLUSPLUSFLAGS' : [
            '<@(common_gcc_cflags_cc)',
            '-stdlib=libc++',
          ],

          'WARNING_CFLAGS': [
            '<@(common_gcc_warning_flags)',
            '-Wtrigraphs', # Disable Xcode default.
          ],

          'OTHER_LDFLAGS': [
            '-framework CoreFoundation',
          ],
        },

        'cflags_cc': [
          '<@(common_gcc_warning_flags)',
          '-Wno-non-virtual-dtor',
#          '-Werror',
          '<@(common_gcc_cflags_cc)',
          '-fno-rtti',
          '-fno-exceptions',
        ],

        'cflags_c': [
          '<@(common_gcc_warning_flags)',
#          '-Werror',
          '<@(common_gcc_cflags_c)',
          '-fno-exceptions',
        ],

        'ldflags': [
          '-Wl,--gc-sections',
        ],

        'target_conditions': [
          ['OS=="mac"', {
            'defines': [
              'DARTINO_TARGET_OS_MACOS',
              'DARTINO_TARGET_OS_POSIX' ],
          }],
          ['OS=="linux"', {
            'defines': [
              'DARTINO_TARGET_OS_LINUX',
              'DARTINO_TARGET_OS_POSIX' ],
          }],
          ['OS=="win"', {
            'defines': [
              'DARTINO_TARGET_OS_WIN' ],
          }],
        ],
      },

      'dartino_release': {
        'abstract': 1,

        'defines': [
          'NDEBUG', # TODO(ahe): Is this necessary/used?
        ],

        'xcode_settings': { # And ninja.
          'OTHER_CPLUSPLUSFLAGS' : [
            '-O3',
            '-fomit-frame-pointer',
            # Strict aliasing optimizations are not safe for the
            # type of VM code that we write. We operate with
            # raw memory aliased with a mixture of pointer types.
            '-fno-strict-aliasing',
          ],
        },

        'msvs_settings': {
          'VCCLCompilerTool': {
            'Optimization': '2',
            'InlineFunctionExpansion': '2',
            'EnableIntrinsicFunctions': 'true',
            'FavorSizeOrSpeed': '0',
            'ExceptionHandling': '0',
            'RuntimeTypeInfo': 'false',
            'StringPooling': 'true',
            'RuntimeLibrary': '0',  # /MT - Multi-threaded, static
          },
          'VCLinkerTool': {
            'LinkIncremental': '1',
            'GenerateDebugInformation': 'true',
            'OptimizeReferences': '2',
            'EnableCOMDATFolding': '2',
            'AdditionalDependencies': [
              'dbghelp.lib',
            ],
          },
        },

        'cflags': [
          '-O3',
          '-fomit-frame-pointer',
          # Strict aliasing optimizations are not safe for the
          # type of VM code that we write. We operate with
          # raw memory aliased with a mixture of pointer types.
          '-fno-strict-aliasing',
        ],
      },

      'dartino_debug': {
        'abstract': 1,

        'defines': [
          'DEBUG',
        ],

        'xcode_settings': { # And ninja.
          'GCC_OPTIMIZATION_LEVEL': '0',

          'OTHER_CFLAGS': [
            '-g',
          ],

          'OTHER_CPLUSPLUSFLAGS': [
            '-g',
          ],
        },

        'msvs_settings': {
          'VCCLCompilerTool': {
            'Optimization': '0',
            'DebugInformationFormat': '3',
            'ExceptionHandling': '0',
            'RuntimeTypeInfo': 'false',
            'RuntimeLibrary': '1',  # /MTd - Multi-threaded, static (debug)
          },
          'VCLinkerTool': {
            'GenerateDebugInformation': 'true',
            'AdditionalDependencies': [
              'dbghelp.lib',
            ],
          },
        },

        'cflags': [
          '-g',
          '-O0',
          # See comment on strict aliasing optimizations above.
          '-fno-strict-aliasing',
        ],
      },

      'dartino_ia32': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_IA32',
        ],

        'cflags': [
          '-m32',
          # Forces GCC to not use x87 floating point instructions.
          '-mfpmath=sse',
          '-msse2',
        ],

        'ldflags': [
          '-m32',
        ],

        'xcode_settings': { # And ninja.
          'ARCHS': [ 'i386' ],
        },
      },

      'dartino_mips': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_MIPS',
        ],

        'cflags_cc': [
          '-Wno-unused-variable',
          '-mips32r2',
          '-EL',
        ],

        'cflags_c':[
          '-Wno-unused-variable',
          '-mips32r2',
          '-EL',
        ],

        'ldflags': [
          '-EL',
        ],

      },

      'dartino_xmips': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_MIPS',
        ],

        'target_conditions': [
          ['_toolset=="target"', {
            'defines': [
              # Fake define intercepted by cc_wrapper.py to change the
              # compiler binary to a MIPS cross compiler. This is only
              # needed on linux.
              'DARTINO_MIPS',
            ],

            'cflags_cc': [
              '-Wno-unused-variable',
              '-mips32r2',
              '-EL',
            ],

            'cflags_c':[
              '-Wno-unused-variable',
              '-mips32r2',
              '-EL',
            ],

            'ldflags': [
              # Fake define intercepted by cc_wrapper.py.
              '-L/DARTINO_MIPS',
              '-EL',
            ],


            'conditions': [
              [ 'OS!="win"', {
                'variables': {
                  'ldso_path%': '<!(/bin/echo -n $LDSO_PATH)',
                  'ld_r_path%': '<!(/bin/echo -n $LD_R_PATH)',
                },
                'conditions': [
                  ['ldso_path!=""', {
                    'ldflags': ['-Wl,--dynamic-linker=<(ldso_path)'],
                  }],
                  ['ld_r_path!=""', {
                    'ldflags': ['-Wl,--rpath=<(ld_r_path)'],
                  }],
                ],
              }],
            ],
          }],

          ['_toolset=="host"', {
            # Compile host targets as IA32, to get same word size.
            'inherit_from': [ 'dartino_ia32' ],

            # The 'dartino_ia32' target will define IA32 as the target. Since
            # the host should still target MIPS, undefine it.
            'defines!': [
              'DARTINO_TARGET_IA32',
            ],
          }],
        ],

      },

      'dartino_x64': {
        'abstract': 1,

        'defines': [
          'DARTINO64',
          'DARTINO_TARGET_X64',
        ],

        # Shared libraries on x64 require compilation with position
        # independent code. Load-time relocation is not supported on
        # x64. For simplicity we compile all x64 libraries with
        # position independent code.
        'cflags': ['-fPIC'],

        'xcode_settings': { # And ninja.
          'ARCHS': [ 'x86_64' ],

          'OTHER_CPLUSPLUSFLAGS': [
            '-fPIC',
          ],
        },
      },

      'dartino_arm': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_ARM',
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'xcode_settings': { # And ninja.
          'ARCHS': [ 'armv7' ],
        },
      },

      'dartino_xarm': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_ARM',
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'target_conditions': [
          ['_toolset=="target"', {
            'conditions': [
              ['OS=="linux"', {
                'defines': [
                  # Fake define intercepted by cc_wrapper.py to change the
                  # compiler binary to an ARM cross compiler. This is only
                  # needed on linux.
                  'DARTINO_ARM',
                 ],
               }],
              ['OS=="mac"', {
                'xcode_settings': { # And ninja.
                  'ARCHS': [ 'armv7' ],

                  'OTHER_CPLUSPLUSFLAGS' : [
                    '-isysroot',
                    '<(ios_sdk_path)',
                  ],

                  'OTHER_CFLAGS' : [
                    '-isysroot',
                    '<(ios_sdk_path)',
                  ],
                },
               }]
            ],

            'ldflags': [
              # Fake define intercepted by cc_wrapper.py.
              '-L/DARTINO_ARM',
              '-static-libstdc++',
            ],
          }],

          ['_toolset=="host"', {
            # Compile host targets as IA32, to get same word size.
            'inherit_from': [ 'dartino_ia32' ],

            # The 'dartino_ia32' target will define IA32 as the target. Since
            # the host should still target ARM, undefine it.
            'defines!': [
              'DARTINO_TARGET_IA32',
            ],
          }],
        ],
      },

      'dartino_xarm64': {
        'abstract': 1,

        'defines': [
          'DARTINO64',
          'DARTINO_TARGET_ARM64',
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'target_conditions': [
          ['_toolset=="target"', {
            'conditions': [
              ['OS=="linux"', {
                'defines': [
                  # Fake define intercepted by cc_wrapper.py to change the
                  # compiler binary to an ARM64 cross compiler. This is only
                  # needed on linux.
                  'DARTINO_ARM64',
                 ],
               }],
              ['OS=="mac"', {
                'xcode_settings': { # And ninja.
                  'ARCHS': [ 'arm64' ],

                  'OTHER_CPLUSPLUSFLAGS' : [
                    '-isysroot',
                    '<(ios_sdk_path)',
                  ],

                  'OTHER_CFLAGS' : [
                    '-isysroot',
                    '<(ios_sdk_path)',
                  ],
                },
               }],
            ],

            'ldflags': [
              # Fake define intercepted by cc_wrapper.py.
              '-L/DARTINO_ARM64',
              '-static-libstdc++',
            ],
          }],

          ['_toolset=="host"', {
            # Compile host targets as X64, to get same word size.
            'inherit_from': [ 'dartino_x64' ],

            # The 'dartino_x64' target will define IA32 as the target. Since
            # the host should still target ARM, undefine it.
            'defines!': [
              'DARTINO_TARGET_X64',
            ],
          }],
        ],
      },

      'dartino_mbed': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_ARM',
          'DARTINO_THUMB_ONLY',
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'target_conditions': [
          ['_toolset=="target"', {
            'defines': [
              'GCC_XARM_EMBEDDED', # Fake define intercepted by cc_wrapper.py.
              'DARTINO_TARGET_OS_CMSIS',
            ],

            'defines!': [
              'DARTINO_TARGET_OS_POSIX',
              'DARTINO_TARGET_OS_LINUX',
              'DARTINO_TARGET_OS_MACOS',
            ],

            'cflags': [
              '-mcpu=cortex-m4',
              '-mthumb',
              '-mfloat-abi=softfp',
              '-fno-common',
            ],

            # Use the gnu language dialect to get math.h constants
            'cflags_c': [
              '--std=gnu99',
            ],

            # Use the gnu language dialect to get math.h constants
            'cflags_cc': [
              '--std=gnu++11',
            ],

            'include_dirs': [
              '<(mbed_path)/rtos/TARGET_CORTEX_M',
            ],

            'ldflags': [
              '-L/GCC_XARM_EMBEDDED', # Fake define intercepted by cc_wrapper.py.
              '-static-libstdc++',
            ],
          }],

          ['_toolset=="host"', {
            # Compile host targets as IA32, to get same word size.
            'inherit_from': [ 'dartino_ia32' ],

            # Undefine IA32 target and using existing ARM target.
            'defines!': [
              'DARTINO_TARGET_IA32',
            ],
          }],
        ],
      },

      'dartino_cortex_m_base': {
        'abstract': 1,

        'defines': [
          'DARTINO32',
          'DARTINO_TARGET_ARM',
          'DARTINO_THUMB_ONLY',
          'DARTINO_SMALL',
        ],

        'target_conditions': [
          ['_toolset=="target"', {
            'variables': {
              'gcc_cflags': [
                '-mthumb',
                '-Wall',
                '-fmessage-length=0',
                '-ffunction-sections',
                # Use -Og here and remove -O0 below as the GCC ARM Embedded
                # compiler cannot compile the cmpctmalloc implementation
                # with -O0.
                '-Og',
              ],

              # Use the gnu language dialect to get math.h constants
              'gcc_cflags_c': [
                '--std=gnu99',
              ],

              # Use the gnu language dialect to get math.h constants
              'gcc_cflags_cc': [
                '--std=gnu++11',
              ],

              'gcc_ldflags': [
                '-mthumb',
                '-Wl,-Map=output.map',
                '-Wl,--gc-sections',
                # Fake define intercepted by cc_wrapper.py.
                '-L/GCC_XARM_EMBEDDED',
                '-static-libstdc++',
              ],
            },

            'defines': [
              'GCC_XARM_EMBEDDED', # Fake define intercepted by cc_wrapper.py.
              'DARTINO_TARGET_OS_CMSIS',
            ],

            'defines!': [
              'DARTINO_TARGET_OS_POSIX',
              'DARTINO_TARGET_OS_LINUX',
              'DARTINO_TARGET_OS_MACOS',
            ],

            'conditions': [
              ['OS=="linux"', {
                'cflags!': [
                  # See comment on -Og above.
                  '-O0',
                ],
                'cflags': [
                  '<@(gcc_cflags)'
                ],
                'cflags_c': [
                  '<@(gcc_cflags_c)'
                ],
                'cflags_cc': [
                  '<@(gcc_cflags_cc)'
                ],
                'ldflags': [
                  '<@(gcc_ldflags)'
                ],
              }],
              ['OS=="mac"', {
                'xcode_settings': {
                  # See comment on -Og above.
                  'GCC_OPTIMIZATION_LEVEL': 'g',
                  # This removes the option -fasm-blocks that GCC ARM Embedded
                  # does not support.
                  'GCC_CW_ASM_SYNTAX': 'NO',
                  # This removes the option -gdwarf-2'.
                  # TODO(sgjesse): Revisit debug symbol generation.
                  'GCC_GENERATE_DEBUGGING_SYMBOLS': 'NO',
                  'OTHER_LDFLAGS!': [
                    '-framework CoreFoundation',
                  ],
                  'OTHER_CFLAGS': [
                    '<@(gcc_cflags)',
                    '<@(gcc_cflags_c)'
                  ],
                  'OTHER_CPLUSPLUSFLAGS!' : [
                    '-stdlib=libc++',
                  ],
                  'OTHER_CPLUSPLUSFLAGS': [
                    '<@(gcc_cflags)',
                    '<@(gcc_cflags_cc)'
                  ],
                  'OTHER_LDFLAGS': [
                    '<@(gcc_ldflags)'
                  ],
                },
              }],
            ],
          }],

          ['_toolset=="host"', {
            # Compile host targets as IA32, to get same word size.
            'inherit_from': [ 'dartino_ia32' ],

            # Undefine IA32 target and using existing ARM target.
            'defines!': [
              'DARTINO_TARGET_IA32',
            ],
          }],
        ],
      },

      'dartino_cortex_m7': {
        'abstract': 1,

        'defines': [
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'variables': {
          'common_cflags_ldflags': [
            '-mcpu=cortex-m7',
            '-mfloat-abi=hard',
            '-mfpu=fpv5-sp-d16',
          ],
        },

        'target_conditions': [
          ['_toolset=="target"', {
            'conditions': [
              ['OS=="linux"', {
                'cflags': [
                  '<@(common_cflags_ldflags)',
                ],
                'ldflags': [
                  '<@(common_cflags_ldflags)',
                ],
              }],
              ['OS=="mac"', {
                'xcode_settings': {
                  'OTHER_CFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_CPLUSPLUSFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_LDFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                },
              }],
            ],
          }],
        ],
      },

      'dartino_cortex_m4f': {
        'abstract': 1,

        'defines': [
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'variables': {
          'common_cflags_ldflags': [
            '-mcpu=cortex-m4',
            '-mfloat-abi=hard',
            '-mfpu=fpv5-sp-d16',
          ],
        },

        'target_conditions': [
          ['_toolset=="target"', {
            'conditions': [
              ['OS=="linux"', {
                'cflags': [
                  '<@(common_cflags_ldflags)',
                ],
                'ldflags': [
                  '<@(common_cflags_ldflags)',
                ],
              }],
              ['OS=="mac"', {
                'xcode_settings': {
                  'OTHER_CFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_CPLUSPLUSFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_LDFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                },
              }],
            ],
          }],
        ],
      },

      'dartino_cortex_m3': {
        'abstract': 1,

        'defines': [
          'DARTINO_TARGET_ARM_SOFTFLOAT'
        ],

        'defines!': [
          'DARTINO_TARGET_ARM_HARDFLOAT'
        ],

        'variables': {
          'common_cflags_ldflags': [
            '-mcpu=cortex-m3',
            '-mfloat-abi=soft',
          ],
        },

        'target_conditions': [
          ['_toolset=="target"', {
            'conditions': [
              ['OS=="linux"', {
                'cflags': [
                  '<@(common_cflags_ldflags)',
                ],
                'ldflags': [
                  '<@(common_cflags_ldflags)',
                ],
              }],
              ['OS=="mac"', {
                'xcode_settings': {
                  'OTHER_CFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_CPLUSPLUSFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                  'OTHER_LDFLAGS': [
                    '<@(common_cflags_ldflags)',
                  ],
                },
              }],
            ],
          }],
        ],
      },

      'dartino_asan': {
        'abstract': 1,

        'cflags': [
          '-fsanitize=address',
        ],

        'defines': [
          'DARTINO_ASAN',
        ],

        'ldflags': [
          '-fsanitize=address',
        ],

        'xcode_settings': { # And ninja.
          'OTHER_CPLUSPLUSFLAGS': [
            '-g3',
            '-fsanitize=address',
            '-fsanitize-undefined-trap-on-error',
          ],

          'OTHER_LDFLAGS': [
            # GYP's xcode_emulation for ninja passes OTHER_LDFLAGS to libtool,
            # which doesn't understand -fsanitize=address. The fake library
            # search path is recognized by cxx_wrapper.py and cc_wrapper.py,
            # which will pass the correct options to the linker.
            '-L/DARTINO_ASAN',
          ],
        },
      },

      'dartino_clang': {
        'abstract': 1,

        'defines': [
          # Recognized by cxx_wrapper.py and cc_wrapper.py and causes them to
          # invoke clang.
          'DARTINO_CLANG',
        ],

        'ldflags': [
          # The define above is not passed to the cxx_wrapper.py and
          # cc_wrapper.py scripts when linking. We therefore have to force
          # the use of clang with a dummy link flag.
          '-L/DARTINO_CLANG',
        ],

        'xcode_settings': { # And ninja.
          'OTHER_LDFLAGS': [
            # Recognized by cxx_wrapper.py and cc_wrapper.py and causes them to
            # invoke clang.
            '-L/DARTINO_CLANG',
          ],
        },
      },

      'dartino_ios_sim': {
        'abstract': 1,
        'conditions': [
          [ 'OS=="mac"', {
            'target_conditions': [
              ['_toolset=="target"', {
                'xcode_settings': {
                  'OTHER_CPLUSPLUSFLAGS' : [
                    '-isysroot',
                    '<(ios_sim_sdk_path)',
                    '-miphoneos-version-min=7.0',
                  ],
                  'OTHER_CFLAGS' : [
                    '-isysroot',
                    '<(ios_sim_sdk_path)',
                    '-miphoneos-version-min=7.0',
                  ],
                },
              }],
            ],
          }],
        ],
      },

      'dartino_use_single_precision': {
        'abstract': 1,

        'defines': [
          'DARTINO_USE_SINGLE_PRECISION',
        ],
      },

      'dartino_disable_live_coding': {
        'abstract': 1,

        'defines!': [
          'DARTINO_ENABLE_LIVE_CODING',
        ],
      },

      'dartino_disable_debugging': {
        'abstract': 1,

        'defines!': [
          'DARTINO_ENABLE_LIVE_CODING',
          'DARTINO_ENABLE_DEBUGGING',
        ],
      },

      'dartino_disable_ffi': {
        'abstract': 1,

        'defines!': [
          'DARTINO_ENABLE_FFI',
        ],
      },

      'dartino_disable_native_processes': {
        'abstract': 1,

        'defines!': [
          'DARTINO_ENABLE_NATIVE_PROCESSES',
        ],
      },

      'dartino_disable_print_interceptors': {
        'abstract': 1,

        'defines!': [
          'DARTINO_ENABLE_PRINT_INTERCEPTORS',
        ],
      },
    },
  },
}
